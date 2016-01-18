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
