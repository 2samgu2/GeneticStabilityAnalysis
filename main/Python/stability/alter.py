"""alter.py.

This file contains a class for various alteration strategies used.

Author -- Terek R Arce
Version -- 2.0
"""

import numpy as np
import os as os
from math import floor
from random import sample, choice, uniform
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import StratifiedKFold
from stability.estimator import Estimator


def select_k_best(k, X, y):
    """Selects the top k features, returning their indices in chi2 rank order.

    :param k: Number of top features to select.
    :param X: The training input samples.
    :param y: The target values (class labels in classification)
    :return: Ranked indices by score.
    """
    b = SelectKBest(chi2, k).fit(X, y)
    a = b.get_support(indices=True)
    a = [x for _, x in sorted(zip(b.scores_[a], a), reverse=True)]
    return np.array(a)


class AlterStrategy:
    """Describes the alteration strategy used."""

    # Alter strategies included:
    ALL = 0
    SUB = 1
    RAND_SUB = 2
    GREEDY = 3

    def __init__(self, strategy, estimator: Estimator = None,
                 X=None, y=None, path=None):
        """Initializes an alter strategy.

        :param strategy: The strategy to be initialized.  e.g. AlterStrategy.ALL
        :param estimator: The estimator (aka classifier) tested by the strategy.
        :param X: The samples. [n_samples, n_features]
        :param y: The classes (aka labels for the samples. [n_samples]
        :param path: The path to a folder to save files to.
        """
        self._type = strategy
        self.estimator = estimator
        self.X = X
        self.y = y
        self.path = path

        if self.type == AlterStrategy.ALL:
            self._name = "ALL"
        elif self.type == AlterStrategy.SUB:
            self._name = "SUB"
        elif self.type == AlterStrategy.RAND_SUB:
            self._name = "RAND_SUB"
        elif self.type == AlterStrategy.GREEDY:
            self._name = "GREEDY"
            filename = '{}greedyRank.npy'.format(self.estimator.name)
            self.greedy_path = os.path.join(path, filename)
            # if a green rank doesn't exist, create one
            if not os.path.exists(self.greedy_path):
                print("GREEDY RANK INITIALIZER - THIS CAN TAKE A WHILE.")
                self.estimator.fit(X, y)
                to_choose = list(range(X.shape[1]))
                chosen = []
                for i in range(X.shape[1]):
                    accuracies = []
                    for idx in to_choose:
                        accuracies.append(self.accuracy(X, y, chosen, idx, self.estimator))
                    a = [x for _, x in sorted(zip(accuracies, to_choose))]
                    chosen.append(a[0])
                    to_choose.remove(a[0])
                np.save(self.greedy_path, chosen)

    @property
    def type(self):
        """Returns the type of the alteration strategy.

        :return: The type of the alteration strategy
        """
        return self._type

    @property
    def name(self):
        """Returns the name of the alteration strategy.

        :return: The string name of the alteration strategy.
        """
        return self._name

    @staticmethod
    def accuracy(X, y, chosen, idx_to_change, estimator: Estimator = None):
        """

        :param X: Test samples.
        :param y: True labels for X.
        :param chosen: Indices chosen so far
        :param idx_to_change: The index to change and test.
        :param estimator: The estimator (aka classifier) used to score the change.
        :return:
        """
        result = []
        for x in X:
            alt = np.copy(x)
            # alter prev chosen
            for i in chosen:
                alt[i] = 0
            # alter new gene
            alt[idx_to_change] = 0
            result.append(alt)
        result = np.array(result)
        return estimator.score(result, y)

    def alter(self, percent, X):
        """Alters a percent of the genes in the Test samples by the alteration strategy.
        Note: Because genes are already ordered by chi2 rank in the main program,
         we can choose top k to alter for the SUB strategy.

        :param percent: The percent of the subset to select from X
        :param X: Test samples.
        :return:
        """
        high = np.amax(self.X)
        low = np.amin(self.X)
        result = []
        k = floor(X[0].size * percent)
        if k <= 0:
            return X
        else:
            indices = []
            if self.type == AlterStrategy.RAND_SUB:
                indices = sample(range(X[0].size), k)
            elif self.type == AlterStrategy.SUB:
                indices = list(range(k))
            elif self.type == AlterStrategy.GREEDY:
                indices = np.load(self.greedy_path)[0:k:1]
            elif self.type == AlterStrategy.ALL:
                indices = list(range(X[0].size))
            for x in X:
                alt = np.copy(x)
                for i in indices:
                    if self.type == AlterStrategy.ALL:
                        offset = alt[i] * percent
                        low = alt[i] - offset
                        high = alt[i] + offset
                        alt[i] = choice([low, high])
                    else:
                        alt[i] = uniform(low, high)
                result.append(alt)
            return np.array(result)

    def cross_validate(self, percent=0, n_splits=10):
        """Performs cross validation of the alteration strategy used for a given
        percentage of genes in the test samples.

        :param percent: The percentage of genes to alter.
        :param n_splits: The number of folds.
        :return: The scores for a given percentage change.
        """
        scores = []
        skf = StratifiedKFold(n_splits)
        for train_index, test_index in skf.split(self.X, self.y):
            self.estimator.fit(self.X[train_index], self.y[train_index])
            accuracy = self.estimator.score(
                self.alter(percent, self.X[test_index]), self.y[test_index])
            scores.append(accuracy)
        return np.array(scores)

    def get_accuracies(self, step=0.05):
        """ Calculates the accuracies for [0,1] at increments of step.  This
        acts as a percentage of the genes to change from 0 to 100%.

        :param step: The step size for the accuracies.
        :return: The accuracies over all steps from 0 to 1
        """
        percents = np.arange(0, 1.01, step)
        accuracies = []
        deviations = []
        for percent in percents:
            scores = self.cross_validate(percent)
            accuracies.append(scores.mean())
            deviations.append(scores.std())
        accuracies = np.array(accuracies)
        deviations = np.array(deviations)
        result = np.column_stack((percents, accuracies, deviations))
        filename = '{}_{}_result.npy'.format(self.estimator.name, self.name)
        np.save(os.path.join(self.path, filename), result)
        return result
