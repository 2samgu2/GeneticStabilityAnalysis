"""nbc.py.

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

from collections import Counter
from math import sqrt
import numpy as np
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import lsqr


class Model:
    """Describes the model class."""

    def __init__(self, samples, eps, label):
        """Initialize the model class.

        Args:
            samples: training samples of size [samples, genes].
            eps: epsilon value for correlation cutoff.
            label: classification label.
        """
        self._label = label
        self._samples = np.array(samples)
        self._genes = range(len(self._samples[0]))

        corr_matrix = np.corrcoef(self._samples, y=None, rowvar=0)
        self._corr_mask = (np.absolute(corr_matrix) > eps)

        self._coeffs = np.array(
            [self._get_coeff(gene) for gene in self._genes])

    def _get_coeff(self, gene):
        """Return the coefficients associated with a gene.

        Returns the coefficients associatd with the system of equation: Ax=b,
        where A is an equation list created from the neighbors of gene n and
        b is the value of gene n.

        Args:
            gene: the gene for which the coefficients are to be calculated.
        Returns:
            A list that is treated as the coefficients for the solution
            to obtian the gene's expression value.
        """
        mask = self._corr_mask[gene]
        sys_eqs = []
        r_side = []
        for sample in self._samples:
            equation = []
            for neighbor in self._genes:
                if mask[neighbor] and neighbor != gene:
                    equation.append(sample[neighbor])
                else:
                    equation.append(0)
            equation.append(1)
            sys_eqs.append(equation)
            r_side.append(sample[gene])
        sys_eqs = np.array(sys_eqs)
        r_side = np.array(r_side)

        solution = lsqr(sys_eqs, r_side)[0]
        return solution.tolist()

    def hypothetical_expr(self, sample):
        """Given a sample, return the hypothetical expression.

        Args:
            sample: the sample whose hypothetical expression we wish to
            calculate
        Returns:
            expr: A list with the expression values of size number of genes.
        """
        sample = np.asarray(sample)
        expr = []
        for gene in self._genes:
            val = 0
            for neighbor in self._genes:
                val += self._coeffs[gene, neighbor] * sample[neighbor]
            val += self._coeffs[gene, len(self._coeffs[gene]) - 1]
            expr.append(val)
        expr = np.array(expr)
        return expr

    def get_label(self):
        """Return the classification label of this model."""
        return self._label


class NetworkBasedClassifier:
    """Describes the NBClassifier class."""

    def __init__(self, eps):
        """Initialize a NBF classifier.

        Args:
            eps: epsilon value
        """
        self._models = []
        self._model_labels = []
        self._eps = eps

    def fit(self, data, classes):
        """Fit the data with classes to create class models.

        Fits the data [num_samples, num_genes] with classifications
        [num_samples] to the model.  Creates as many models as classes.

        Args:
            data: the samples we wish to train the classifier on
            classes: the classifications associated with the samples
        """
        data = np.asarray(data)
        classes = np.asarray(classes)

        for key in Counter(classes):
            a_class = np.where(classes == key)
            samples = np.array([data[i] for i in a_class[0]])
            self._models.append(Model(samples, self._eps, key))
            self._model_labels.append(key)

    def predict(self, samples):
        """Predict the classification of a sample.

        Must fit the classifier before this method is called.

        Args:
            samples: the samples we wish to predict classification for.

        Returns:
            classifications: the classifications of the samples.
        """
        classifications = []

        for sample in samples:
            errors = []
            labels = []
            for model in self._models:
                labels.append(model.get_label())
                predicted = np.asarray(model.hypothetical_expr(sample))
                mse = mean_squared_error(sample, predicted)
                rmse = sqrt(mse)
                errors.append(rmse)
            i = errors.index(min(errors))
            classifications.append(labels[i])

        return np.array(classifications)
