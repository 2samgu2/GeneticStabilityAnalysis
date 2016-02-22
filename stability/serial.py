"""serial.py.

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
from stability.classifier import create, accuracy

def getClassifiers ( type, indices, classes, exprs, folds = 10 ) :
    tmp = [ create ( type, indices, classes, exprs, fold ) for fold in range (folds) ]
    classifiers = [ c[1] for c in tmp ]
    return classifiers

def avgAccuracy ( classifiers, indices, classes, exprs, change, test, series, folds = 10, repeats = 10 ):
    avg = 0
    for r in range( repeats ):
        avg += accuracy ( classifiers, indices, classes, exprs, change, test, series )
    avg = avg / repeats
    return avg
