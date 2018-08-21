"""alter.py.

Author -- Terek R Arce
Version -- 2.0
"""

import numpy as np
import os as os
from math import floor
from random import sample, choice, uniform
from multiprocessing import Pool, cpu_count
from sklearn.model_selection import StratifiedKFold
from stability.estimator import Estimator
from typing import Optional


class AlterStrategy:
    """Describes the alteration strategy used."""
    estimator: Optional[Estimator]

    # Alter strategies included:
    ALL = 0
    SUB = 1
    RAND_SUB = 2
    GREEDY = 3

    def __init__(self,
                 _type,
                 estimator: Estimator = None,
                 X=None, y=None,
                 path=None):
        self._type = _type
        self.estimator = estimator
        self.X = X
        self.y = y
        if self.type == AlterStrategy.ALL:
            self._name = "ALL"
        elif self.type == AlterStrategy.SUB:
            self._name = "SUB"
        elif self.type == AlterStrategy.RAND_SUB:
            self._name = "RANDSUB"
        elif self.type == AlterStrategy.GREEDY:
            self._name = "GREEDY"
            filename = '{}greedyRank.npy'.format(estimator.name)
            self.greedy_path = os.path.join(path, filename)
            if not os.path.exists(self.greedy_path):
                print("GREEDY RANK INITIALIZER - THIS CAN TAKE A WHILE.")
                self.estimator.fit(X, y)
                to_choose = list(range(X.shape[1]))
                chosen = []
                for i in range(X.shape[1]):
                    pool = Pool(processes=cpu_count())
                    accuracies = pool.starmap(
                        self.accuracy,
                        [(X, y, chosen, idx, self.estimator) for idx in to_choose])
                    pool.terminate()
                    a = [x for _, x in sorted(zip(accuracies, to_choose))]
                    chosen.append(a[0])
                    to_choose.remove(a[0])
                np.save(self.greedy_path, chosen)

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    def accuracy(self,
                 X, y,
                 chosen, idx_to_change,
                 estimator: Estimator=None):
        # TODO: run multiple times and return avg accuracy
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
        """B/c genese are already ordered by chi2 rank we can choose top k to alter.

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
                        # alt[i] = choice([0, alt[i] * 2])
                        alt[i] = uniform(low, high)
                result.append(alt)
            return np.array(result)

    def cross_validate(self, percent=0, cv=10):
        scores = []
        skf = StratifiedKFold(cv)
        for train_index, test_index in skf.split(self.X, self.y):
            self.estimator.fit(self.X[train_index], self.y[train_index])
            accuracy = self.estimator.score(
                self.alter(percent, self.X[test_index]), self.y[test_index])
            scores.append(accuracy)
        return np.array(scores)

    def get_accuracies(self, step=0.05):
        percents = np.arange(0, 1.01, step)
        accuracies = []
        deviations = []
        for percent in percents:
            scores = self.cross_validate(percent)
            accuracies.append(scores.mean())
            deviations.append(scores.std())
        accuracies = np.array(accuracies)
        deviations = np.array(deviations)
        return np.column_stack((percents, accuracies, deviations))
