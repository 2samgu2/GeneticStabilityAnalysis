# This is the R script for importing series data.  For the notebook version
# with more information on how it works, see SIT.ipynb in the notebooks folder.

library(GEOquery)
library(affy)
library(simpleaffy)

gc()

# Note that command args will need to changed according to where you
# are running the script from.
# If running from command line:
#args <- commandArgs(trailingOnly=TRUE)
# If running from R console:
# overwrite with: commandArgs <- function() c("GSE7079","rgu34a")
args <- commandArgs(trailingOnly=TRUE)

notebook_dir <- getwd() # get the working directory
main_dir <- dirname(dirname(notebook_dir)) # get two levels up
gse_dir = file.path(main_dir,"GSE")
if (!dir.exists(gse_dir)) {
    dir.create(gse_dir)
}

paste("Downloading GEO series...")
gse <- getGEO(GEO = series, destdir = gse_dir)
if(length(gse) > 1) {
    print("WARNING: multiple SubSeries.")
}

series.pheno <- phenoData(gse[[1]])

if (!dir.exists(file.path(gse_dir, series))) {
    paste("Downloading supplementary files...)
    suppFiles = getGEOSuppFiles(GEO = series, makeDirectory = TRUE, baseDir = gse_dir)
    tarFiles = file.path(rownames(suppFiles)[1])
    untarPath = file.path(dirname(tarFiles),"data")
    if (!dir.exists(file.path(untarPath))) {
        paste("Unpacking tar...")
        untar(tarFiles, exdir = untarPath)
    }
}

setwd(file.path(gse_dir,series,"data")) # TODO: convert series to upper case.
celfiles.data = ReadAffy()

paste("Downloading probe data...")
probe_name = annotation(celfiles.data)
lib <- paste(probe_name, ".db", sep = "")
source("https://bioconductor.org/biocLite.R")
biocLite(lib)
library(lib, character.only=TRUE)

celfiles.rma <- rma(celfiles.data)
celfiles.filtered_rma <- nsFilter(celfiles.rma, require.entrez=TRUE, remove.dupEntrez=TRUE)

rma_mat <- exprs(celfiles.filtered_rma[[1]])
colnames(rma_mat) <- pData(series.pheno)$title

setwd(gse_dir)
result_path = file.path(gse_dir,series,"filteredRMA.txt")
write.table(rma_mat,result_path,sep = "\t", row.names=TRUE)
