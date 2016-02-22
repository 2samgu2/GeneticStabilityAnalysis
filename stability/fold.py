"""fold.py.

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
from collections import Counter
from sklearn.cross_validation import KFold

def kFoldInd ( classes, k ):

    training_data_indices = []
    test_data_indices = []
    num_classes = 0
    for label in Counter(classes):
        num_classes += 1
        a_class = np.where( classes == label )
        a_class = a_class[0]

        kf = KFold( len( a_class ), k )
        for train_index, test_index in kf:
            training_data_indices.append( [ a_class[i] for i in train_index ] )
            test_data_indices.append( [ a_class[i] for i in test_index ] )

    training = []
    test = []

    for i in range( k ):
        combo_test = []
        combo_train = []
        for j in range ( num_classes ):
            combo_test += test_data_indices [ i + (k * j) ]
            combo_train += training_data_indices [ i + (k * j) ]
        combo_test.sort()
        combo_train.sort()
        test.append(combo_test)
        training.append(combo_train)

    return np.array(training), np.array(test)
