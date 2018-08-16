# Run SIT first with GSE19804 to ensure the series is imported

notebook_dir <- getwd() # get the working directory
main_dir <- dirname(dirname(notebook_dir)) # get two levels up
gse_dir = file.path(main_dir,"GSE","GSE19804")

setwd(gse_dir)

paste("Reading in filtered RMA data")
matrix <- read.table("filteredRMA.txt",header=TRUE,row.names=1)

paste("Cleaning up...")
classes <- gsub("Lung.", "", colnames(matrix))
classes = gsub("\\..*","",classes)

colnames(matrix) <- classes

paste("Generating classes and data...")
patterns <- c("Cancer", "Normal")
expressions = matrix[ , grepl( paste(patterns, collapse="|") , names( matrix ) ) ]

classes = gsub("\\..*","",colnames(expressions))
classes = as.matrix(classes)
classes = t(classes)
write.table(classes,file.path(gse_dir,"classes.txt"),sep = "\t", quote = FALSE, row.names=FALSE, col.names=FALSE)

expressions = t(expressions)
write.table(expressions,file.path(gse_dir,"exprs.txt"),sep = "\t", row.names=FALSE, col.names=FALSE)

paste("Expressions and classes generated successfully.")
