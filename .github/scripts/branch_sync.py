#!/usr/bin/env python3
"""Bring every branch up to date with the base branch, and report what happened to each.

WHY THIS EXISTS
  Branches here live for months. `dev-themes` sat 153 commits behind master and — because
  GitHub resolves push-triggered workflows from the file ON THE PUSHED BRANCH — it was missing
  `publish-branch.yml` entirely, so four pushes in August produced no build and no failure. Nothing
  reported it because nothing ran. This job runs from the DEFAULT branch on a schedule, so it cannot
  be disabled by a branch that lacks it, which is the whole point.

THE LADDER, per branch, cheapest and least destructive first:
  1. up-to-date       — already contains base, nothing to do
  2. fast-forward     — branch has no commits of its own: no rewrite, no merge commit, no force
  3. merge            — appends a merge commit; every clone stays an ancestor, so `git pull` still
                        fast-forwards and nobody has to reset anything
  4. conflict         — reported with the conflicting paths, never forced, never left half-applied

MERGE IS THE DEFAULT, deliberately. Rebase would keep history linear but rewrites it and force-
pushes, which diverges every existing clone; worse, it replays the branch's own commits on every
run, so the same conflict can resurface nightly, where a merge records the resolution once.
`--strategy rebase` is there for a branch you want linearised: it tries rebase first and falls back
to a merge when the replay conflicts, and pushes with --force-with-lease so a push that landed
underneath is refused rather than clobbered.

The status file is the product. It is written whether or not anything changed, so an in-estate agent
can read one artifact and know the state of every branch — see services/theming/branch_sync_watch.py
in moprox-tooling, which posts conflicts to Discord.
"""
import argparse, json, os, subprocess, sys, datetime

BOT_BRANCHES = ["totolo-merge-proposed"]      # machine-managed by merge_proposed_with_totolo.yaml


def git(*args, check=True, cwd=None):
    r = subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)
    if check and r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), (r.stderr or r.stdout).strip()[:400]))
    return r


def out(*args, **kw):
    return git(*args, **kw).stdout.strip()


def branches(remote, base, exclude):
    names = []
    for ln in out("for-each-ref", "--format=%(refname:short)", "refs/remotes/%s" % remote).splitlines():
        name = ln.split("/", 1)[1] if "/" in ln else ln
        if name in ("HEAD", base) or name in exclude or ln == remote:
            continue
        names.append(name)
    return sorted(set(names))


def divergence(remote, base, branch):
    """(ahead, behind) — commits the branch has that base doesn't, and vice versa."""
    left, right = out("rev-list", "--left-right", "--count",
                      "%s/%s...%s/%s" % (remote, base, remote, branch)).split()
    return int(right), int(left)


def conflicted_paths(cwd=None):
    return sorted(set(out("diff", "--name-only", "--diff-filter=U", cwd=cwd).splitlines()))


def sync_one(remote, base, branch, strategy, dry_run, workdir):
    """Run the ladder for one branch inside its own worktree. Returns a status dict."""
    ahead, behind = divergence(remote, base, branch)
    rec = {"branch": branch, "ahead": ahead, "behind": behind,
           "last_commit": out("log", "-1", "--format=%cs", "%s/%s" % (remote, branch)),
           "action": None, "pushed": False, "conflict_files": [], "error": None}
    if behind == 0:
        rec["action"] = "up-to-date"
        return rec

    wt = os.path.join(workdir, branch.replace("/", "__"))
    git("worktree", "add", "--detach", wt, "%s/%s" % (remote, branch))
    try:
        git("checkout", "-B", "sync/%s" % branch, "%s/%s" % (remote, branch), cwd=wt)

        if ahead == 0:                                    # nothing of its own: clean fast-forward
            git("merge", "--ff-only", "%s/%s" % (remote, base), cwd=wt)
            rec["action"] = "fast-forwarded"
            force = False
        else:
            rebased = False
            if strategy == "rebase":
                r = git("rebase", "%s/%s" % (remote, base), cwd=wt, check=False)
                if r.returncode == 0:
                    rebased = True
                else:
                    # Capture what actually clashed BEFORE aborting — after the abort it is gone.
                    rec["conflict_files"] = conflicted_paths(cwd=wt)
                    git("rebase", "--abort", cwd=wt, check=False)
            if rebased:
                rec["action"] = "rebased"; force = True
            else:
                r = git("merge", "--no-edit", "%s/%s" % (remote, base), cwd=wt, check=False)
                if r.returncode == 0:
                    rec["action"] = "merged"; rec["conflict_files"] = []; force = False
                else:
                    rec["conflict_files"] = rec["conflict_files"] or conflicted_paths(cwd=wt)
                    git("merge", "--abort", cwd=wt, check=False)
                    rec["action"] = "conflict"
                    # The asymmetry runs BOTH ways, measured on this repo: a rebase can conflict
                    # mid-replay where one merge is clean, and a merge can conflict where a rebase
                    # applies (misc-collections, 2026-08-27 -- rebase replays each commit against a
                    # moving base and can recognise work already upstream, a merge sees one diff
                    # against one ancestor). So when merge fails, probe a rebase READ-ONLY and say
                    # whether it would have worked. Nothing is pushed either way; it just tells the
                    # human whether `strategy=rebase` on this one branch is the cheap way out.
                    if strategy == "merge":
                        r = git("rebase", "%s/%s" % (remote, base), cwd=wt, check=False)
                        rec["rebase_would_apply"] = r.returncode == 0
                        git("rebase", "--abort", cwd=wt, check=False)
                        git("reset", "--hard", "%s/%s" % (remote, branch), cwd=wt, check=False)
                    return rec

        if dry_run:
            rec["pushed"] = False
            rec["error"] = "dry-run: not pushed"
            return rec
        push = ["push", remote, "HEAD:refs/heads/%s" % branch]
        if force:
            # --force-with-lease, pinned to the SHA we started from: a push that landed while we
            # were rebasing refuses rather than being overwritten.
            push.insert(1, "--force-with-lease=refs/heads/%s:%s"
                        % (branch, out("rev-parse", "%s/%s" % (remote, branch))))
        r = git(*push, check=False)
        if r.returncode == 0:
            rec["pushed"] = True
        else:
            rec["error"] = (r.stderr or r.stdout).strip()[:300]
            rec["action"] = "push-rejected"     # protected branch, or someone pushed underneath us
    except Exception as exc:
        rec["action"] = rec["action"] or "error"
        rec["error"] = str(exc)[:300]
    finally:
        git("worktree", "remove", "--force", wt, check=False)
        git("branch", "-D", "sync/%s" % branch, check=False)
    return rec


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="master")
    p.add_argument("--remote", default="origin")
    p.add_argument("--strategy", choices=["merge", "rebase"], default="merge",
                   help="'merge' never rewrites history (default); 'rebase' tries rebase, falls back to merge")
    p.add_argument("--exclude", default=",".join(BOT_BRANCHES))
    p.add_argument("--max-age-days", type=int, default=365,
                   help="skip branches whose last commit is older than this (0 = no limit). Ancient "
                        "branches conflict on every run and would make the report pure noise.")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--status-out", default="branch-sync-status.json")
    p.add_argument("--workdir", default=".branch-sync")
    a = p.parse_args()

    exclude = {x.strip() for x in a.exclude.split(",") if x.strip()}
    git("fetch", "--prune", a.remote)
    os.makedirs(a.workdir, exist_ok=True)
    today = datetime.date.today()

    results = []
    for br in branches(a.remote, a.base, exclude):
        last = out("log", "-1", "--format=%cs", "%s/%s" % (a.remote, br))
        age = (today - datetime.date.fromisoformat(last)).days
        if a.max_age_days and age > a.max_age_days:
            ahead, behind = divergence(a.remote, a.base, br)
            results.append({"branch": br, "ahead": ahead, "behind": behind, "last_commit": last,
                            "action": "skipped-stale", "pushed": False, "conflict_files": [],
                            "error": "last commit %d days ago (> %d)" % (age, a.max_age_days)})
            continue
        results.append(sync_one(a.remote, a.base, br, a.strategy, a.dry_run, a.workdir))

    for br in sorted(exclude):
        results.append({"branch": br, "action": "skipped-excluded", "pushed": False,
                        "conflict_files": [], "error": None, "ahead": None, "behind": None,
                        "last_commit": None})

    tally = {}
    for r in results:
        tally[r["action"]] = tally.get(r["action"], 0) + 1
    status = {"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "repo": os.environ.get("GITHUB_REPOSITORY", ""),
              "run_url": "%s/%s/actions/runs/%s" % (os.environ.get("GITHUB_SERVER_URL", ""),
                                                    os.environ.get("GITHUB_REPOSITORY", ""),
                                                    os.environ.get("GITHUB_RUN_ID", "")),
              "base": a.base, "base_sha": out("rev-parse", "%s/%s" % (a.remote, a.base))[:12],
              "strategy": a.strategy, "dry_run": a.dry_run,
              "summary": tally, "branches": results}
    with open(a.status_out, "w") as f:
        json.dump(status, f, indent=1)

    w = max([len(r["branch"]) for r in results] + [6])
    print("%-*s %-16s %6s %6s  %s" % (w, "branch", "action", "ahead", "behind", "detail"))
    for r in sorted(results, key=lambda r: (r["action"] != "conflict", r["branch"])):
        detail = ",".join(r["conflict_files"][:3]) or (r["error"] or "")
        print("%-*s %-16s %6s %6s  %s" % (w, r["branch"], r["action"], r["ahead"], r["behind"], detail[:70]))
    print("\nsummary:", json.dumps(tally))
    return 0            # conflicts are data, not a failed job — the watcher decides what to do


if __name__ == "__main__":
    sys.exit(main())
