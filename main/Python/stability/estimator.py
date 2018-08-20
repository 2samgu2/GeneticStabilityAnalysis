"""estimator.py.

This file contains a wrapper class for classifiers used.


Author -- Terek R Arce
Version -- 2.0
"""

from stability.nbc import NetworkBasedClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB


class Estimator:
    """Describes the classifier chooser."""

    # Classifiers included:
    NBC = 0
    KNN = 1
    SVM = 2
    RF = 3
    NB = 4
    
    def __init__(self, _type, epsilon=0.8, k=1):
        """Initializes the classifier type.

        :param _type: The type of classifier to initialize.
        :param epsilon: Used in NBC (See nbc.py for more details).
        :param k: Used in KNeighborsClassifier (See documentation for more details).
        """
        self._type = _type

        # create the classifier
        if self.type == Estimator.NBC:
            self._classifier = NetworkBasedClassifier(epsilon)
            self._name = "NBC"
        elif self.type == Estimator.KNN:
            self._classifier = KNeighborsClassifier(k)
            self._name = "KNN"
        elif self.type == Estimator.SVM:
            self._classifier = svm.LinearSVC()
            self._name = "SVM"
        elif self.type == Estimator.RF:
            self._classifier = RandomForestClassifier()
            self._name = "RF"
        elif self.type == Estimator.NB:
            self._classifier = GaussianNB()
            self._name = "NB"
    
    @property
    def type(self):
        """Returns the type of the classifier.

        :return: The type of the classifier
        """
        return self._type
    
    @property
    def name(self):
        """Returns the name of the classifier.

        :return: The string name of the classifier.
        """
        return self._name
    
    def fit(self, X, y):
        """Fit the model using X as training data and y as target values.

        :param X: Training data. If array or matrix, shape [n_samples, n_features].
        :param y: Target values of shape = [n_samples]
        """
        self._classifier.fit(X, y)
        
    def score(self, X, y):
        """Returns the mean accuracy on the given test data and labels.

        :param X: Test samples
        :param y: True labels for X
        :return: Mean accuracy of self.predict(X) wrt. y.
        """
        return self._classifier.score(X, y)
        
    def predict(self, X):
        """Predict the class labels for the provided data.

        :param X: Test samples.
        :return: lass labels for each data sample.
        """
        return self._classifier.predict(X)