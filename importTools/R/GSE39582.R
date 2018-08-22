# Run SIT first with GSE39582 to ensure the series is imported

notebook_dir <- getwd() # get the working directory
main_dir <- dirname(dirname(notebook_dir)) # get two levels up
gse_dir = file.path(main_dir,"GSE","GSE39582")

setwd(gse_dir)

paste("Reading in filtered RMA data")
matrix <- read.table("filteredRMA.txt",header=TRUE,row.names=1)

paste("Reading series data...")
library(GEOquery)
gse <- getGEO(GEO = 'GSE39582', destdir = dirname(gse_dir))

paste("Cleaning up...")
pheno <-phenoData(gse[[1]])
colnames(matrix)<-pheno$characteristics_ch1.30

classes <- gsub("cit.molecularsubtype: ", "", colnames(matrix))
colnames(matrix) <- classes

colnames(matrix) <- classes

paste("Generating classes and data...")
patterns <- c("C1","C2","C3","C4","C5","C6")
expressions = matrix[ , grepl( paste(patterns, collapse="|") , names( matrix ) ) ]

classes = gsub("\\..*","",colnames(expressions))
classes = as.matrix(classes)
classes = t(classes)
write.table(classes,file.path(gse_dir,"classes.txt"),sep = "\t", quote = FALSE, row.names=FALSE, col.names=FALSE)

expressions = t(expressions)
write.table(expressions,file.path(gse_dir,"expressions.txt"),sep = "\t", row.names=FALSE, col.names=FALSE)

paste("Expressions and classes generated successfully.")
