"""nbc.py.

This file contains classes for the Network-based Classifier.

Author -- Terek R Arce
Version -- 2.0
"""

import numpy as np
from multiprocessing import Pool, cpu_count
from collections import Counter
from math import sqrt
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import lsqr


class Model:
    """The model constructed for a given class"""

    def __init__(self, X, label, epsilon=0.8):
        """Initializes the model for a given class.

        :param X: Training data for model. If array or matrix, shape [n_samples, n_features].
        :param label: Class label for the data.
        :param epsilon: Correlation cutoff value.
        """
        self._label = label
        self.X = np.array(X)

        correlations = np.corrcoef(self.X, y=None, rowvar=False)

        # Note: the mask is the graph.
        self.mask = (np.absolute(correlations) > epsilon)
        print(np.sum(self.mask[0]))

        pool = Pool(processes=cpu_count())
        self.coefficients = pool.starmap(self.solver,
                                         [(gene, self.mask[gene], self.X) for gene in range(len(correlations))])
        pool.terminate()

        self.coefficients = np.array(self.coefficients)
        print("NBC Model constructed.")

    @staticmethod
    def solver(gene, mask, X):
        """Uses least-square solver to compute coefficients for Ax=b, where
        A is an equation list created from the neighbors of a gene and b is
        the value of the gene.

        :param gene: The index of the gene to be solved for.
        :param mask: The correlation mask for the gene.
        :param X: The training samples.
        :return: The coefficients of the equation (x) in Ax=b
        """
        A = []
        b = []
        for sample in X:
            neighbors = [sample[neighbor] if (mask[neighbor] and (gene != neighbor))
                         else 0
                         for neighbor in range(len(mask))]
            neighbors.append(1)
            A.append(neighbors)
            b.append(sample[gene])
        A = np.array(A)
        b = np.array(b)
        x = lsqr(A, b)[0]
        return x.tolist()

    def expression(self, sample):
        """Returns a hypothetical expression level for a given sample.

        :param sample: Test sample
        :return: The hypothetical expression level of a given sample.
        """
        expression = []
        for gene in range(len(self.coefficients)):
            level = 0  # the expression level of a gene
            for neighbor in range(len(self.mask) - 1):
                level += self.coefficients[gene][neighbor] * sample[neighbor]
            level += self.coefficients[gene][len(self.mask)]
            expression.append(level)
        return np.array(expression)

    def label(self):
        """Returns the class label of the model.

        :return: The class label of the model.
        """
        return self._label


class NetworkBasedClassifier:
    """Classifier implementing the Network-based Classifier."""

    def __init__(self, epsilon=0.8):
        """Initializes the classifier.

        :param epsilon: epsilon value correlation cutoff.
        """
        self.models = []
        self.epsilon = epsilon

    def fit(self, X, y):
        """Fit the model using X as training data and y as target values.

        :param X: Training data. If array or matrix, shape [n_samples, n_features].
        :param y: Target values of shape = [n_samples]
        """
        self.models = []
        y = np.array(y)
        X = np.array(X)
        for label in Counter(y):
            a_class = np.where(y == label)
            self.models.append(Model([X[i] for i in a_class[0]], label, self.epsilon))

    def predict(self, X):
        """Predict the class labels for the provided data.

        :param X: Test samples.
        :return: Class labels for each data sample.
        """
        pool = Pool(processes=cpu_count())
        classifications = pool.map(self.classification, [sample for sample in X])
        pool.terminate()
        return classifications

    def score(self, X, y):
        """Returns the mean accuracy on the given test data and labels.

        :param X: Test samples.
        :param y: True labels for X.
        :return: Mean accuracy of self.predict(X) wrt. y.
        """
        y = np.array(y)
        X = np.array(X)
        correct = np.asarray(self.predict(X) == y)
        return np.sum(correct) / correct.shape[0]

    def classification(self, sample):
        """Returns the classification of the sample.

        :param sample: Test sample
        :return: The class label of the sample.
        """
        errors = []
        for model in self.models:
            error = sqrt(mean_squared_error(sample, model.expression(sample)))
            errors.append(error)
        min_index = errors.index(min(errors))
        return self.models[min_index].label()
