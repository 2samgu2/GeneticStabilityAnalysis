"""alter.py.

Author -- Terek R Arce
Version -- 2.0
"""


class AlterStrategy:
    """Describes the alteration strategy used."""

    # Alter strategies included:
    ALL = 0
    SUB = 1
    RANDSUB = 2
    GREEDY = 3

    def __init__(self,
                 _type):
        self._type = _type
        if _type == AlterStrategy.ALL:
            self._name = "ALL"
        elif _type == AlterStrategy.SUB:
            self._name = "SUB"
        elif _type == AlterStrategy.RANDSUB:
            self._name = "RANDSUB"
        elif _type == AlterStrategy.GREEDY:
            self._name = "GREEDY"

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def Accuracy(estimator, X, y, chosen, idx_to_change):
        # TODO: run multiple times and return avg accuracy
        result = []
        for x in X:
            alt = np.copy(x)
            # alter prev chosen
            for i in chosen:
                # alt[i] = choice([0, alt[i]*2])
                alt[i] = 0
            # alter new gene
            # alt[idx_to_change] = choice([0, alt[idx_to_change]*2])
            alt[idx_to_change] = 0
            result.append(alt)
        result = np.array(result)
        return estimator.score(result, y)

    '''Static method'''

    def RankGreedy(estimator, X, y):
        fileName = '{}greedyRank.npy'.format(estimator.getName())
        if (path.exists(path.join(gsa_path, fileName))):
            return
        print("GREEDY RANK INITIALIZER - THIS CAN TAKE A WHILE.")
        estimator.fit(X, y)
        notChosen = list(range(X.shape[1]))
        chosen = []
        for i in range(X.shape[1]):
            pool = mp.Pool(processes=mp.cpu_count())
            accuracy = pool.starmap(AlterStrategy.Accuracy, [(estimator, X, y, chosen, idx) for idx in notChosen])
            pool.terminate()
            a = [x for _, x in sorted(zip(accuracy, notChosen))]
            chosen.append(a[0])
            notChosen.remove(a[0])
        np.save(path.join(gsa_path, fileName), chosen)

    def Subset(percent, X):
        """
        B/c genese are already ordered by chi2 rank we can choose top k to alter.
        """
        result = []
        idx = floor(X[0].size * percent)
        if idx <= 0:
            return X
        else:
            for x in X:
                alt = np.copy(x)
                for i in range(idx):
                    alt[i] = choice([0, alt[i] * 2])
                result.append(alt)
            return np.array(result)

    def RandSubset(percent, X):
        result = []
        k = floor(X[0].size * percent)
        if k <= 0:
            return X
        else:
            indices = sample(range(X[0].size), k)
            for x in X:
                alt = np.copy(x)
                for i in indices:
                    alt[i] = choice([0, alt[i] * 2])
                result.append(alt)
            return np.array(result)

    def All(percent, X):
        print(percent)
        result = []
        for x in X:
            print(x)
            alt = []
            for gene in x:
                _offset = gene * percent
                _low = gene - _offset
                _high = gene + _offset
                alt.append(choice([_low, _high]))
            result.append(alt)
            print(alt)
        return np.array(result)

    def Greedy(percent, X, estimator):
        high = np.amax(X)
        low = np.amin(X)
        result = []
        k = floor(X[0].size * percent)
        if k <= 0:
            return X
        else:
            file = path.join(gsa_path, '{}greedyRank.npy'.format(estimator.getName()))
            indices = np.load(file)
            for x in X:
                alt = np.copy(x)
                for i in indices[0:k:1]:
                    alt[i] = uniform(low, high)
                result.append(alt)
            return np.array(result)

    def Alter(self, percent, X, estimator):
        if self._type == AlterStrategy.ALL:
            return AlterStrategy.All(percent, X)
        elif self._type == AlterStrategy.SUB:
            return AlterStrategy.Subset(percent, X)
        elif self._type == AlterStrategy.RANDSUB:
            return AlterStrategy.RandSubset(percent, X)
        elif self._type == AlterStrategy.GREEDY:
            return AlterStrategy.Greedy(percent, X, estimator)
