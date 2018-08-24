# Genetic Stability Analysis
This program tests the stability of various machine learning algorithms used in gene expression classificatoin.  It serves as a basis for future stability testing and can be easily extended.

### File Descriptions:

```bash
├── tools
│   ├── r
│   │   ├── GSE****.R
│   │   └── SIT.R
│   ├── notebooks
│   ├── images
│   ├── index.html
│   ├── js
│   │   ├── **/*.js
│   └── partials/template
├── main
│   ├── notebooks
│   └── python
│
│
├── .gitignore
├── LICENSE
└── README.md
```

The entry point for testing MLA stability begins with importing training data.  To do this, use the Stability Import Tool (SIT) progrma.  There are two versions of the program: a iPyhton notebook version and an R version.  Use either to import data from NCBI GEO to be used in the stability analysis.  See... for examples of good datasets to use and a description of the type of datasets to use.  

analysis of various machine learning algorithms over expression data.

Start point is SPA, Followed by custom GSE.R script (See examples of data used)

Once imported, run main.

TODO: rename to GenAlgoStabilty
