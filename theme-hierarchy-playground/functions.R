## theme hierarchy print function
generate_dag <- function(infile) {
  mydata <- read.delim(file = infile, sep = ",", header = TRUE, stringsAsFactors = FALSE)
  duplicate_themes <- mydata[duplicated(mydata[, "Theme"]), "Theme"]
  no_of_duplicate_themes <- length(duplicate_themes)

  for (i in 1:no_of_duplicate_themes) {
    mytheme <- duplicate_themes[i]
    theme_indices <- which(mydata[, "Theme"] == mytheme)
    no_of_duplicates <- length(theme_indices)
    mydata[theme_indices, "Theme"] <- paste0(mytheme, "::", 1:no_of_duplicates)
  }

  root_theme <- "literary theme"
  prune_method <- "simple"
  limit <- nrow(mydata)
  theme_id <-  which(mydata[, "Theme"] == root_theme)
  child_ids <- which(mydata[, "ParentTheme"] == root_theme)
  no_of_child_ids <- length(child_ids)
  node_ids <- c(theme_id, child_ids)

  while (no_of_child_ids >= 1) {
    child_id <- child_ids[1]
    child_ids <- child_ids[-1]
	grandchild_ids <- which(mydata[, "ParentTheme"] == mydata[child_id, "Theme"])
    no_of_grandchild_ids <- length(grandchild_ids)

	if (no_of_grandchild_ids >= 1) {
      node_ids <- unique(c(node_ids, grandchild_ids))
	}

    child_ids <- unique(c(child_ids, grandchild_ids))
      no_of_child_ids <- length(child_ids)
    }

    no_of_node_ids <- length(node_ids)
    leaf_ids <- numeric()

    for (i in 1:no_of_node_ids) {
      node_id <- node_ids[i]
      node <- mydata[node_id, "Theme"]
      if (node%in%mydata[, "ParentTheme"] == FALSE) {
        leaf_ids <- c(leaf_ids, node_id)
      }
    }

    no_of_leaf_ids <- length(leaf_ids)
    path_strings <- character(no_of_leaf_ids)

    for (i in 1:no_of_leaf_ids) {
      path_string <- character()
      leaf_id <- leaf_ids[i]
      thistheme <- mydata[leaf_id, "Theme"]

      while (thistheme != root_theme) {
        path_string <- c(thistheme, path_string)
        thistheme <- mydata[which(mydata[, "Theme"] == thistheme), "ParentTheme"]
      }

    path_string <- c(root_theme, path_string)
    path_strings[i] <- paste(path_string, collapse = "/")
  }

  subdata <- data.frame(Theme = mydata[leaf_ids, "Theme"], pathString = path_strings)
  tree <- as.Node(subdata)
  return(tree)
}

## convert a brainstorming table in csv format to a Cytoscape readable file
table_to_dot_2 <- function(infile, outfile) {
  mydata <- read.delim(file = infile, sep = ",", header = TRUE, stringsAsFactors = FALSE)
  duplicate_themes <- mydata[duplicated(mydata[, "Theme"]), "Theme"]
  no_of_duplicate_themes <- length(duplicate_themes)

  for (i in 1:no_of_duplicate_themes) {
    mytheme <- duplicate_themes[i]
    theme_indices <- which(mydata[, "Theme"] == mytheme)
    no_of_duplicates <- length(theme_indices)
    mydata[theme_indices, "Theme"] <- paste0(mytheme, "::", 1:no_of_duplicates)
  }

  out <- data.frame(
    source <- mydata[-1, 3],
    target <- mydata[-1, 1],
    stringsAsFactors = FALSE
  )

  colnames(out) <- c("source", "target")
  no_of_edges <- nrow(out)

  write("digraph MultiStep {\n\n  rankdir=LR;\n", file = outfile)

  for (i in 1:no_of_edges) {
    source <- out[i, 1]
    target <- out[i, 2]
    write(paste0(c("  \"", source, "\" -> \"", target, "\";"), collapse = ""), file = outfile, append = TRUE)
  }

  write("\n}", file = outfile, append = TRUE)
}

## convert a brainstorming table in csv format to a dot file
table_to_dot <- function(infile, outfile) {
  # preliminaries
  mydata <- read.delim(file = infile, sep = ",", header = TRUE, stringsAsFactors = FALSE)
  no_of_edges <- nrow(mydata)
  duplicate_themes <- mydata[duplicated(mydata[, "Child"]), "Child"]
  no_of_duplicate_themes <- length(duplicate_themes)

  if (no_of_duplicate_themes > 0) {
    stop("duplicate theme")
  }

  write("digraph MultiStep {\n\n  rankdir=LR;\n", file = outfile)

  for (i in 1:no_of_edges) {
    parent <- mydata[i, "Parent"]
    child <- mydata[i, "Child"]
    write(paste0(c("  \"", parent, "\" -> \"", child, "\";"), collapse = ""), file = outfile, append = TRUE)
  }

  write("\n}", file = outfile, append = TRUE)
}










