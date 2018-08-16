# files should be put in FIT directory
# if running from R console overwrite FIT.R with: commandArgs <- function() c("GSE27562","hgu133plus2")


process <- function(matrix, name)
{
  # Get only 3 classes
  colsNames <- union( grep("normal", colnames(matrix), value = TRUE ), grep("malignant", colnames(matrix), value = TRUE ))
  colsNames <- union( colsNames, grep("benign", colnames(matrix), value = TRUE ))
  
  # remove PBMC_ from matrix
  result_matrix <- gsub("PBMC_", "", colnames(matrix) )
  
  col_numbers <- rev(c(1:10))
  
  # remove "_training_" from matrix
  t_col_numbers <- paste(c("_training_"), col_numbers, sep = '', collapse = ' ')
  t_col_numbers <- unlist(strsplit(t_col_numbers, split=" "))
  
  for (i in 1:length(t_col_numbers) )
  {
      result_matrix <- sub(t_col_numbers[i][1], "", result_matrix)
  }
  
  col_numbers <- rev(c(1:47))
  
  # remove "_validation_" from matrix
  t_col_numbers <- paste(c("_validation_"), col_numbers, sep = '', collapse = ' ')
  t_col_numbers <- unlist(strsplit(t_col_numbers, split=" "))
  
  for (i in 1:length(t_col_numbers) )
  {
      result_matrix <- sub(t_col_numbers[i][1], "", result_matrix)
  }

  # Create classes
  write.table(result_matrix, paste(name, "_GSE27562_ts_classes.txt",
  sep=""), sep = "\t", row.names=FALSE, col.names=FALSE)
  
  # Get data from only 3 classes
  colsNumbers <- union( grep("normal", colnames(matrix), value = FALSE ), grep("malignant", colnames(matrix), value = FALSE ))
  colsNumbers <- union( colsNames, grep("benign", colnames(matrix), value = FALSE ))
  
  data <- matrix[colsNumbers]

  # Create data
  write.table(data, paste(name, "_GSE27562_ts_data.txt", sep=""),
  sep = "\t", row.names=FALSE, col.names=FALSE)
}

setwd("~/Downloads/RFiles/GSE27562")

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
