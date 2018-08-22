# Run SIT first with GSE27562 to ensure the series is imported

notebook_dir <- getwd() # get the working directory
main_dir <- dirname(dirname(notebook_dir)) # get two levels up
gse_dir = file.path(main_dir,"GSE","GSE27562")

setwd(gse_dir)

paste("Reading in filtered RMA data")
matrix <- read.table("filteredRMA.txt",header=TRUE,row.names=1)

paste("Cleaning up...")
classes <- gsub("PBMC_", "", colnames(matrix))

toRemove <- rev(c(1:10))
toRemove <- paste(c("_training_"), toRemove, sep = '', collapse = ' ')
toRemove <- unlist(strsplit(toRemove, split=" "))
for (i in 1:length(toRemove)) {
    classes <- sub(toRemove[i][1], "", classes)
}

toRemove <- rev(c(1:47))
toRemove <- paste(c("_validation_"), toRemove, sep='', collapse=' ')
toRemove <- unlist(strsplit(toRemove, split=" "))
for (i in 1:length(toRemove))
{
    classes <- sub(toRemove[i][1], "", classes)
}

colnames(matrix) <- classes

paste("Generating classes and data...")
patterns <- c("normal", "benign", "malignant")
expressions = matrix[ , grepl( paste(patterns, collapse="|") , names( matrix ) ) ]

classes = gsub("\\..*","",colnames(expressions))
classes = as.matrix(classes)
classes = t(classes)
write.table(classes,file.path(gse_dir,"classes.txt"),sep = "\t", quote = FALSE, row.names=FALSE, col.names=FALSE)

expressions = t(expressions)
write.table(expressions,file.path(gse_dir,"expressions.txt"),sep = "\t", row.names=FALSE, col.names=FALSE)

paste("Expressions and classes generated successfully.")
