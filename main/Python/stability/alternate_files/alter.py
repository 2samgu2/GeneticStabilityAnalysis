"""alter.py.

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

import numpy as np
from random import uniform


class AlterStrategy:
    """Allows for different ways to alter gene expression values."""
    GREEDY = 0
    CHI2 = 1
    RAND = 2
    PERCENT = 3

    def __init__(self, exprs):
        """Initialize the AlterStrategy.

        Args:
            exprs: the current gene expressions
        """
        self._exprs = exprs

    def alter_all(self, percent):
        """Alter expressions by a given percent.

        Args:
            percent:
        """
        result = []
        for expr in self._exprs:
            alt = []
            for gene in expr:
                off = gene * percent
                low = gene - off
                high = gene + off
                alt.append(uniform(low, high))
            result.append(alt)
        return np.array(result)

    def get_rand_exprs(self):
        """Get random expressions between min and max of current expressions.

        Args:
            exprs: the current expression values.
        """
        high = np.amax(self._exprs)
        low = np.amin(self._exprs)
        rand_exps = []
        for exp in self._exprs:
            new_exp = []
            for gene in exp:
                new_exp.append(uniform(low, high))
            rand_exps.append(new_exp)
        return np.array(rand_exps)

    def alter_subset(self, exprs, indices, series, change):
        """Alter a subset of the expression values.

        Args:
            indices:
        """
        high = np.amax(exprs)
        low = np.amin(exprs)

        # NOTE: indices in the file refers to the
        # num of features being selected
        if change == 1:
            file = ("FASTR/%s_%03d_%03d_nCk.npy" %
                    (series, len(exprs[0]), indices))
            indices = np.load(file)
        elif change == 2:
            file = ("FASTR/%s_%03d_%03d_nCk_rand.npy" %
                    (series, len(exprs[0]), indices))
            indices = np.load(file)

        result = []
        for exp in exprs:
            alt = [g for g in exp]
            for i in indices:
                alt[i] = uniform(low, high)
            result.append(alt)
        return np.array(result)


    def get_unstable_genes(self, exps, percentage, indices):
        if (percentage == 0):
            return exps

        high = np.amax(exps)
        low = np.amin(exps)

        alt_indices = indices[:floor(percent * len(altered_indices))]
        alt_indices.sort()

        print (len(alt_indices))

        rand_exps = []
        for exp in exps:
            new_exp = []
            j = 0
            for i in range( len( exp ) ):
                if (j < len(alt_indices) ):
                    if ( i==alt_indices[j] ):
                        new_exp.append( uniform( low, high ) )
                        j += 1
                    else:
                        new_exp.append(exp[i])
                else:
                    new_exp.append(exp[i])
            rand_exps.append( new_exp )
        return np.array( rand_exps )

"""
change == 0 --> greedy selection
change == 1 --> chi2 selection
change == 2 --> random selection

exprs : the expressions to be altered
indices :
    if 0 then greedily selected indices
    if 1 or 2 then number of indices to be changed
        NOTE that the selection FASTR files are pre-computed TODO: possibly calculate on the fly
series: series for loading file (1 or 2 only)
change: what subset alteration will be performed
"""
