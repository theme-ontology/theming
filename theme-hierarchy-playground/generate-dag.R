## preliminaries
rm(list = ls())
library(data.tree)
library(listviewer)
working_dir <- paste0("/Users/Paul/Dropbox/theming/theme-hierarchy-playground/")
setwd(working_dir)
source("functions.R")
set.seed(12345)
writeLines(capture.output(sessionInfo()), con = "analyze_sessionInfo.txt")

## generate dag
infile <- "my-theme-table-sci-fi.csv"
dag <- generate_dag(infile)
l <- ToListSimple(dag)
jsonedit(l)
#print(tree, pruneMethod = prune_method, limit = limit)






table_to_cytoscape(infile)


