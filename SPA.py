"""
SPA.py.
Author -- Terek R Arce
Version -- 1.0

Copyright © 2016 Terek Arce
"""

import sys
import getopt
import numpy as np
from stability.testing import greedy, chi2rand
from stability.write import writeFile
from stability.classifier import getType
from stability.alter import getChange
import time

"""
change == 0 --> greedy selection
change == 1 --> chi2 selection
change == 2 --> random selection
"""


def main(argv):
    try:
        opts, args = getopt.getopt( argv, "ht:c:" ,[ "type=","change=" ] )
    except getopt.GetoptError:
        print ( "SPA.py -t <classifier type> -c <change strategy>" )
        print ( "-h for HELP" )
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print ( "SPA.py -t <classifier type> -c <change strategy>" )
            print ( "The following classifiers are available:" )
            print ( "knn, svm, nbc, nb, rf ")
            print ( "The follwoing alteration algorithms are available:" )
            print ( "greedy, chi2, rand, percent")
            sys.exit()
        elif opt in ("-t", "--type"):
            strType = arg
        elif opt in ("-c", "--change"):
            strChange = arg

    name = strType.lower() + "_" + strChange.lower()
    series = [ "GSE19804", "GSE39582", "GSE27562"]
    num_folds = 10
    num_repeats = 10
    size = 100
    sub_features = np.arange( 0, 1.01, 0.05 ) # or percentage
    type = getType( strType )
    change = getChange ( strChange )

    data = [series, size, sub_features.tolist(), num_folds, num_repeats]

    accuracy_series = []
    for s in series:
        file_name = ( "/cise/research64/terek/FutureConfStability/SPA/test_%s_%s.txt" % ( name, s ) )
        fname = ( "/cise/research64/terek/FutureConfStability/SPA/data_%s_%s.npy" % ( name, s ) )

        if ( change == 0 ):
            selected = greedy (s, size, type, change)

        elif (change == 1 or change == 2 or change == 3 ):
            selected = chi2rand ( sub_features, s, size, type, change )

        writeFile ( file_name, data, fname, selected)

if __name__ == "__main__":
    main(sys.argv[1:])
