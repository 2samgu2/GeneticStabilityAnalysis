"""
nbc.py.

Author -- Terek R Arce
Version -- 1.0
"""

from collections import Counter
from math import sqrt
import numpy as np
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import lsqr


class Model:
    """Describes the model class."""

    def __init__(self, samples, eps, class_label):
        """Initialize the model class.

        Args:
            samples: training samples of size [samples, genes].
            eps: epsilon value for correlation cutoff.
            class_label: classification label.
        """

        self.class_label = class_label
        self.samples = np.array(samples)
        self.eps = eps

        self.correlation = np.corrcoef( self.samples, y=None, rowvar=0, bias=0, ddof=None ) # columns are variables, rows are samples

        self.mask = (np.absolute(self.correlation) > self.eps)  # note that the mask is actually the graph

        # the coefficients associated with the system of equation: Ax=b,
        # where A is an equation list created from the neighbors of gene
        # n and b is the value of gene n.
        self.geneFuncMasks = []  # these are the coefficients in Ax=b
        for gene in range(len(self.correlation)):
            currMask = self.mask[gene]
            setOfNeighbors = []
            solutions = []
            for sample in self.samples:
                neighbors = [sample[neighbor] if ((currMask[neighbor] == True) and (gene != neighbor)) else 0 for neighbor in range(len(currMask))]
                neighbors.append(1)
                setOfNeighbors.append(neighbors)
                solutions.append(sample[gene])
            coeff = self.AxbSolver(setOfNeighbors, solutions, 2)
            self.geneFuncMasks.append(coeff.tolist())

        self.coefficients = np.array(self.geneFuncMasks)

    def AxbSolver(self, neighbors, sols, choice):
        # Use lsqr to solve Ax=b
        A=np.array(neighbors)
        b=np.array(sols)
        x = lsqr(A,b)[0]
        return x

    def getExpression(self, sample):
        """Given a sample, return the hypothetical expression.

        Args:
            sample: the sample whose hypothetical expression we wish to
            calculate
        Returns:
            expr: A list with the expression values of size number of genes.
        """
        expression = []
        for gene in range(len(self.coefficients)):
            geneVal = 0
            for neighbor in range(len(self.mask)-1):
                geneVal += self.coefficients[gene][neighbor] * sample[neighbor]
            geneVal += self.coefficients[gene][len(self.mask)]
            expression.append(geneVal)
        return np.array(expression)

    def getClass (self):
        """Return the classification label of this model."""
        return self.class_label


class NetworkBasedClassifier:
    """Describes the NBClassifier class."""

    def __init__(self, epsilon):
        """Initialize a NBF classifier.

        Args:
            eps: epsilon value
        """
        self.models = []
        self.epsilon = epsilon

    def fit ( self, X, y ):
        """Fit the data with classes to create class models.

        Fits the data [num_samples, num_genes] with classifications
        [num_samples] to the model.  Creates as many models as classes.

        Args:
            X: the data we wish to train the classifier on
            y: the classifications associated with the samples
        """
        y = np.array(y)
        X = np.array(X)
        for key in Counter(y):
            a_class = np.where(y == key)
            self.models.append(Model([X[i] for i in a_class[0]], self.epsilon, key))

    def predict(self, X):
        """Predict the classification of a sample.

        Must fit the classifier before this method is called.

        Args:
            samples: the samples we wish to predict classification for.

        Returns:
            classifications: the classifications of the samples.
        """
        classifications = []
        for sample in X:
            RMSEs = []
            for model in self.models:
                rmse = sqrt( mean_squared_error(sample, model.getExpression(sample)))
                RMSEs.append(rmse)
            min_index = RMSEs.index(min(RMSEs))
            label = self.models[min_index].getClass()
            classifications.append(label)
        return np.array(classifications)
