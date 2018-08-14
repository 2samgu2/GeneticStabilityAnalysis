# files should be put in FIT directory
# if running from R console overwrite FIT.R with: commandArgs <- function() c("GSE33315","hgu133a")


process <- function(matrix, name)
{
  # Get 7 classes (Hyperdiploid, TCF3-PBX1, ETV6_RUNX1, MLL, PH, Hypodiploid and T-ALL)
  colsNames1 <- union( grep("HYPER", colnames(matrix), value = TRUE ), grep("HYPO", colnames(matrix), value = TRUE ))
  colsNames2 <- union( grep("MLL", colnames(matrix), value = TRUE ), grep("PH", colnames(matrix), value = TRUE ))
  colsNames3 <- union( grep("TALL", colnames(matrix), value = TRUE ), grep("TCF3-PBX1", colnames(matrix), value = TRUE ))
  colsNames <- union(colsNames1, colsNames2)
  colsNames <- union(colsNames, colsNames3)
  colsNames <- union( colsNames, grep("ETV6_RUNX1", colnames(matrix), value = TRUE ))
  
  # Rename Hyperdiploid columns
  HYPERcolNames <- rev(grep("HYPER", colsNames, value = TRUE ))
  
  for (val in HYPERcolNames)
  {
      colsNames <- gsub(val, "Hyperdiploid", colsNames)
  }
  
  # Rename Hypodiploid columns
  HYPOcolNames <- rev(grep("HYPO", colsNames, value = TRUE ))
  
  for (val in HYPOcolNames)
  {
      colsNames <- gsub(val, "Hypodiploid", colsNames)
  }
  
  # Rename MLL columns
  MLLcolNames <- rev(grep("MLL", colsNames, value = TRUE ))
  
  for (val in MLLcolNames)
  {
      colsNames <- gsub(val, "MLL", colsNames)
  }
  
  # Rename PH columns
  PHcolNames <- rev(grep("PH", colsNames, value = TRUE ))
  
  for (val in PHcolNames)
  {
      colsNames <- gsub(val, "PH", colsNames)
  }
  
  # Rename T-ALL columns
  TALLcolNames <- rev(grep("TALL", colsNames, value = TRUE ))
  
  for (val in TALLcolNames)
  {
      colsNames <- gsub(val, "T-ALL", colsNames)
  }
  
  # Rename TCF3-PBX1 columns
  TCF3PBX1colNames <- rev(grep("TCF3-PBX1", colsNames, value = TRUE ))
  
  for (val in TCF3PBX1colNames)
  {
      colsNames <- gsub(val, "TCF3-PBX1", colsNames)
  }
  
  # Rename ETV6_RUNX1 columns
  ETV6RUNX1colNames <- rev(grep("ETV6_RUNX1", colsNames, value = TRUE ))
  
  for (val in ETV6RUNX1colNames)
  {
      colsNames <- gsub(val, "ETV6_RUNX1", colsNames)
  }
  
  # Create classes
  write.table(colsNames, paste(name, "_GSE33315_ts_classes.txt",
  sep=""), sep = "\t", row.names=FALSE, col.names=FALSE)
  
  # Get data from 7 classes (Hyperdiploid, TCF3-PBX1, ETV6_RUNX1, MLL, PH, Hypodiploid and T-ALL)
  colsNumbers1 <- union( grep("HYPER", colnames(matrix), value = FALSE ), grep("HYPO", colnames(matrix), value = FALSE ))
  colsNumbers2 <- union( grep("MLL", colnames(matrix), value = FALSE ), grep("PH", colnames(matrix), value = FALSE ))
  colsNumbers3 <- union( grep("TALL", colnames(matrix), value = FALSE ), grep("TCF3-PBX1", colnames(matrix), value = FALSE ))
  colsNumbers <- union(colsNumbers1, colsNumbers2)
  colsNumbers <- union(colsNumbers, colsNumbers3)
  colsNumbers <- union( colsNumbers, grep("ETV6_RUNX1", colnames(matrix), value = FALSE ))
  
  data <- matrix[colsNumbers]

  # Create data
  write.table(data, paste(name, "_GSE33315_ts_data.txt", sep=""),
  sep = "\t", row.names=FALSE, col.names=FALSE)
}

setwd("~/Downloads/RFiles/GSE33315")

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
