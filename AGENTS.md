# AI Contributor Code of Conduct

These rules apply to **any AI agent or AI-assisted automation** contributing to this repository.
They exist so that automated changes are always reviewed by a human before they land. Humans
contributing in the normal way are unaffected.

## Rules

1. **Never commit or push directly to a protected branch.** Do **not** push to `master` or to any
   `dev-*` branch. Changes to those branches happen **only** through a pull request that a human
   reviews and merges.

2. **Do your work on a feature branch**, named with the prefix **`ai-feature-`**
   (e.g. `ai-feature-add-vampire-theme`). One logical change per branch.

3. **Propose changes via pull request.** Open a PR from your `ai-feature-…` branch into `master` and
   leave it for human review. **Do not merge your own PR**, and never bypass branch protection.

4. **Never force-push** a shared branch and never rewrite published history.

5. For everything else (data format, commit messages, scope), follow the human
   [Contributing Guide](CONTRIBUTING.md).
