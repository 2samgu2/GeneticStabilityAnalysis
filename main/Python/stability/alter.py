"""alter.py.

Author -- Terek R Arce
Version -- 2.0
"""
from typing import Optional

import numpy as np
import os as os
from math import floor
from random import sample, choice
from multiprocessing import Pool, cpu_count
from stability.estimator import Estimator


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
                 path=None,
                 X=None,
                 y=None):
        self._type = _type
        if self.type == AlterStrategy.ALL:
            self._name = "ALL"
        elif self.type == AlterStrategy.SUB:
            self._name = "SUB"
        elif self.type == AlterStrategy.RAND_SUB:
            self._name = "RANDSUB"
        elif self.type == AlterStrategy.GREEDY:
            self._name = "GREEDY"
            filename = '{}greedyRank.npy'.format(estimator.getName())
            self.greedy_path = os.path.join(path, filename)
            if not os.path.exists(self.greedy_path):
                print("GREEDY RANK INITIALIZER - THIS CAN TAKE A WHILE.")
                self.estimator.fit(X, y)
                print(X.shape[1])
                to_choose = list(range(X.shape[1]))
                chosen = []
                for i in range(X.shape[1]):
                    pool = Pool(processes=cpu_count())
                    accuracies = pool.starmap(
                        self.accuracy,
                        [(X, y, chosen, idx, estimator) for idx in to_choose])
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

    def alter(self, percent, X):
        """B/c genese are already ordered by chi2 rank we can choose top k to alter.

        :type rand: bool to select indices randomly or not.  If not, will use chi2 rank.
        :param percent: The percent of the subset to select from X
        :param X: Test samples.
        :return:
        """
        # high = np.amax(X)
        # low = np.amin(X)
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
                        alt[i] = choice([0, alt[i] * 2])
                result.append(alt)
            return np.array(result)

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
