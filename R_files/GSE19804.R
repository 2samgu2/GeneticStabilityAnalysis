# files should be put in FIT directory
# if running from R console overwrite FIT.R with: commandArgs <- function() c("GSE19804","hgu133plus2")

process <- function(matrix, name)
{
  # remove Lung from matrix
  result_matrix <- gsub("Lung.", "", colnames(matrix) )
  
  col_numbers <- c(2,3,6,17,32,33,37,40,43,79,91,92,94,97,102,103,106,109,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,139,142,143,144,145,146,148,149,152,154,156,157,158,159,165,167,177,179,189)
  col_numbers <- rev(col_numbers)
  
  # remove [numbers]T from matrix
  t_col_numbers <- paste(c("."), col_numbers, sep = '', collapse = ' ')
  t_col_numbers <- unlist(strsplit(t_col_numbers, split=" "))
  t_col_numbers <- paste(t_col_numbers, c("T"), sep = '', collapse = ' ')
  t_col_numbers <- unlist(strsplit(t_col_numbers, split=" "))
  
  for (i in 1:length(t_col_numbers) )
  {
      result_matrix <- sub(t_col_numbers[i][1], "", result_matrix)
  }
  
  # remove [numbers]N from matrix
  n_col_numbers <- gsub("T", "N", t_col_numbers)
  for (i in 1:length(n_col_numbers) )
  {
      result_matrix <- gsub(n_col_numbers[i][1], "", result_matrix)
  }
  
  #create classes
  write.table(result_matrix, paste(name, "_GSE19804_ts_classes.txt",
  sep=""), sep = "\t", row.names=FALSE, col.names=FALSE)

  write.table(matrix, paste(name, "_GSE19804_ts_data.txt", sep=""),
  sep = "\t", row.names=FALSE, col.names=FALSE)

}

setwd("~/Downloads/RFiles/GSE19804")

matrix.gcrma <- read.table("gcrma_mat.txt",header=TRUE,row.names=1)
matrix.rma <- read.table("rma_mat.txt",header=TRUE,row.names=1)
matrix.mas5 <- read.table("mas5_mat.txt",header=TRUE,row.names=1)
matrix.orig <- read.table("orig_mat.txt",header=TRUE,row.names=1)
matrix.gcrma_filt<- read.table("gcrma_mat_filt.txt",header=TRUE,row.names=1)
matrix.rma_filt <- read.table("rma_mat_filt.txt",header=TRUE,row.names=1)
matrix.mas5_filt <- read.table("mas5_mat_filt.txt",header=TRUE,row.names=1)

process(matrix.mas5, "mas5")
process(matrix.orig, "orig")
process(matrix.rma, "rma")
process(matrix.gcrma, "gcrma")
process(matrix.rma_filt, "rma_filt")
process(matrix.gcrma_filt, "gcrma_filt")
process(matrix.mas5_filt, "mas5_filt")
