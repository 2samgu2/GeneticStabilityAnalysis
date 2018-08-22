"""GSA.py.

This file contains the main program to run the genetic stability analysis.

Author -- Terek R Arce
Version -- 2.0
"""

import sys
import getopt
import numpy as np
from stability.alter import select_k_best, AlterStrategy
from stability.estimator import Estimator
from os import path, getcwd, makedirs


def main(argv):

    series = ""
    feature_size = 0

    try:
        opts, args = getopt.getopt(argv, "hs:n:", ["type=", "change="])
    except getopt.GetoptError:
        print("SPA.py -s <GSE series number> -n <number of genes>")
        print("-h for HELP")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("SPA.py -s <GSE series number> -n <number of genes>")
            print("Series should be in all capitals.")
            print("See python notebook for details on code.")
            sys.exit()
        elif opt in ("-s", "--series"):
            series = arg
        elif opt in ("-n", "--number"):
            feature_size = arg

    # setup directories
    notebook_dir = getcwd()
    main_dir = path.dirname(path.dirname(notebook_dir))
    load_path = path.join(main_dir, "GSE", series)
    gsa_path = path.join(main_dir, "GSA", series, str(feature_size))
    if not path.exists(gsa_path):
        makedirs(gsa_path)

    # load expressions and classes
    y = np.loadtxt(path.join(load_path, "classes.txt"), dtype=np.str, delimiter="\t")
    X = np.loadtxt(path.join(load_path, "expressions.txt"), delimiter="\t")

    a = select_k_best(feature_size, X, y)
    X = X[:, a]

    np.save(path.join(gsa_path, "expressions.npy"), X)
    np.save(path.join(gsa_path, "classes.npy"), y)

    # calculate stability of classifiers
    estimators = [Estimator(Estimator.KNN),
                  Estimator(Estimator.SVM),
                  Estimator(Estimator.RF),
                  Estimator(Estimator.NB),
                  Estimator(Estimator.NBC)]

    for estimator in estimators:
        strategies = [AlterStrategy(AlterStrategy.ALL, estimator, X, y, gsa_path),
                      AlterStrategy(AlterStrategy.SUB, estimator, X, y, gsa_path),
                      AlterStrategy(AlterStrategy.RAND_SUB, estimator, X, y, gsa_path),
                      AlterStrategy(AlterStrategy.GREEDY, estimator, X, y, gsa_path)]
        for strategy in strategies:
            result = strategy.get_accuracies()
            print(result)


if __name__ == "__main__":
    main(sys.argv[1:])
