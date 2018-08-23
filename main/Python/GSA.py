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
from matplotlib.pyplot import savefig, subplots


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

    # Optional: graph result
    classifiers = ['KNN', 'SVM', 'RF', 'NB', 'NBC']
    strategies = ['ALL', 'SUB', 'RAND_SUB', 'GREEDY']
    names = ['All', 'Chi2 Subset', 'Random Subset', 'Greedy']

    fig, axs = subplots(1, len(strategies), figsize=(16, 4), sharey=True)

    i = 0
    for strategy in strategies:
        for classifier in classifiers:
            data = np.load(path.join(gsa_path, "{}_{}_result.npy".format(classifier, strategy)))
            data = list(zip(*list(data)))
            axs[i].plot(np.arange(0, 101, 5), np.array(data[1]) * 100, label=classifier)
            axs[i].set_xlim(0, 100)
            axs[i].set_title(names[i])
            axs[i].set_xlabel("Altered")
            values = axs[i].get_xticks()
            axs[i].set_xticklabels(['{}%'.format(int(x)) for x in values])
        handles, labels = axs[i].get_legend_handles_labels()
        i = i + 1

    axs[0].set_ylabel("Accuracy")
    values = axs[0].get_yticks()
    axs[0].set_yticklabels(['{}%'.format(int(x)) for x in values])

    fig.legend(handles, labels, loc=3, bbox_to_anchor=(0.35, 1.0, 0.3, 0),
               ncol=len(classifiers), mode="expand", borderaxespad=0.)

    fig.tight_layout()

    savefig('results.png', bbox_inches='tight')


if __name__ == "__main__":
    main(sys.argv[1:])
