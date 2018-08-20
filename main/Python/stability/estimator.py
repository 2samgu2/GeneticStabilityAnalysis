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


import numpy as np
import stability.alter as alter
from stability.nbc import NetworkBasedClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm

"""
type == 0 --> NBC
type == 1 --> kNN
type == 2 --> SVM
type == 3 --> RF
type == 4 --> NB
"""

def getType ( str ):
    types = [ "nbc", "knn", "svm", "rf", "nb" ]
    return types.index( str.lower() )

def init ( type ):
    if (type == 0):
        neigh = NetworkBasedClassifier( 0.8 )
    elif (type == 1):
        neigh = KNeighborsClassifier( n_neighbors = 1 )
    elif ( type == 2 ):
        neigh = svm.LinearSVC()
    elif ( type == 3 ):
        neigh = RandomForestClassifier()
    elif ( type == 4 ):
        neigh = GaussianNB()
    else :
        neigh = KNeighborsClassifier( n_neighbors = 1 )
    return neigh

def train ( jump, indices, classes, exprs, fold ):
    e = np.array( [ exprs[i] for i in indices[fold] ] )
    c = np.array( [ classes[i] for i in indices[fold] ] )
    jump.fit( e, c )
    return (fold, jump)

def create ( type, indices, classes, exprs, fold ):
    c = init ( type )
    return train ( c, indices, classes, exprs, fold )

"""
change == 0 --> greedy selection
change == 1 --> chi2 selection
change == 2 --> random selection
"""
def predict ( a_classifier, indices, classes, exprs, fold, change, test, series ):
    e = np.array( [exprs[i] for i in indices[fold]] )
    c = np.array( [classes[i] for i in indices[fold]] )

    if ( change == 0 or change == 1 or change == 2 ):
        e = alter.subset( e, test, series, change )
    elif( change == 3 ):
        e = alter.all( e, test )

    c_pred = np.array( a_classifier.predict( e ) )

    mask = c_pred == c
    return sum( mask )

def accuracy ( a_classifiers, indices, classes, exprs, change, test, series, folds = 10 ):
    total = 0
    for fold in range( folds ):
        total += predict ( a_classifiers[fold], indices, classes, exprs, fold, change, test, series )
    accuracy = total / len( classes )
    return accuracy
