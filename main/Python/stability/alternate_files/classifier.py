"""classifier.py.

Author -- Terek R Arce
Version -- 1.0

Copyright 2016 Terek Arce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from stability.nbc import NetworkBasedClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm


class MyClassifier:
    """Describes the classifier chooser."""

    # Classifiers included in the chooser
    NBC = 0
    kNN = 1
    SVM = 2
    RM = 3
    NB = 4

    def __init__(self,
                 classifier_type,
                 data,
                 classes,
                 epsilon=0.8,
                 n_neighbors=1):
        """Initialize a NBF classifier.

        Args:
            eps: epsilon value
        """
        self._classifier = None

        # create the classifier
        if classifier_type == MyClassifier.NBC:
            self._classifier = NetworkBasedClassifier(epsilon)
        elif (classifier_type == MyClassifier.kNN):
            self._classifier = KNeighborsClassifier(n_neighbors)
        elif (classifier_type == MyClassifier.SVM):
            self._classifier = svm.LinearSVC()
        elif (classifier_type == MyClassifier.RM):
            self._classifier = RandomForestClassifier()
        elif (classifier_type == MyClassifier.NB):
            self._classifier = GaussianNB()
        else:
            self._classifier = KNeighborsClassifier(n_neighbors)

        # train the classifier
        self._classifier.fit(data, classes)

    def predict(self, samples):
        """Predict class of samples.

        Args:
            samlples:
        """
        return self._classifier.predict(samples)
