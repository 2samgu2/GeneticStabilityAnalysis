# files should be put in FIT directory
# if running from R console overwrite FIT.R with: commandArgs <- function() c("GSE32474","hgu133plus2")


process <- function(matrix, name)
{
  # Get 8 classes (Breast, Central Nervous System, Colon, Leukemia, Melanoma, Non-Small Cell Lung, Ovarian, Renal) except for Prostate
  colsNames <- setdiff( colnames(matrix), grep("PR", colnames(matrix), value = TRUE ))
  
  # Rename Leukemia columns
  LEcolNames <- rev(grep("LE", colsNames, value = TRUE ))
  
  for (val in LEcolNames)
  {
      colsNames <- gsub(val, "Leukemia", colsNames)
  }
  
  # Rename Colon columns
  COcolNames <- rev(grep("CO", colsNames, value = TRUE ))
  
  for (val in COcolNames)
  {
      colsNames <- gsub(val, "Colon", colsNames)
  }
  
  # Rename Breast columns
  BRcolNames <- rev(grep("BR", colsNames, value = TRUE ))
  
  for (val in BRcolNames)
  {
      colsNames <- gsub(val, "Breast", colsNames)
  }
  
  # Rename Central Nervous System columns
  CNScolNames <- rev(grep("CNS", colsNames, value = TRUE ))
  
  for (val in CNScolNames)
  {
      colsNames <- gsub(val, "Central Nervous System", colsNames)
  }
  
  # Rename Melanoma columns
  MEcolNames <- rev(grep("ME", colsNames, value = TRUE ))
  
  for (val in MEcolNames)
  {
      colsNames <- gsub(val, "Melanoma", colsNames)
  }
  
  # Rename Ovarian columns
  OVcolNames <- rev(grep("OV", colsNames, value = TRUE ))
  
  for (val in OVcolNames)
  {
      colsNames <- gsub(val, "Ovarian", colsNames)
  }
  
  # Rename Renal columns
  REcolNames <- rev(grep("RE", colsNames, value = TRUE ))
  
  for (val in REcolNames)
  {
      colsNames <- gsub(val, "Renal", colsNames)
  }
  
  # Rename Non-Small Cell Lung columns
  LCcolNames <- rev(grep("LC", colsNames, value = TRUE ))
  
  for (val in LCcolNames)
  {
      colsNames <- gsub(val, "Non-Small Cell Lung", colsNames)
  }
  
  # Create classes
  write.table(colsNames, paste(name, "_GSE32474_ts_classes.txt",
  sep=""), sep = "\t", row.names=FALSE, col.names=FALSE)
  
  # Get data from 8 classes (Breast, Central Nervous System, Colon, Leukemia, Melanoma, Non-Small Cell Lung, Ovarian, Renal) except for Prostate
  colsNumbers <- setdiff( grep("", colnames(matrix), value = FALSE), grep("PR", colnames(matrix), value = FALSE ))
  data <- matrix[colsNumbers]

  # Create data
  write.table(data, paste(name, "_GSE32474_ts_data.txt", sep=""),
  sep = "\t", row.names=FALSE, col.names=FALSE)
}

setwd("~/Downloads/RFiles/GSE32474")

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
