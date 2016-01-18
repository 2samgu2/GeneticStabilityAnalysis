import numpy as np
import multiprocessing as mp
from stability.classifier import create, accuracy

def getClassifiers ( type, indices, classes, exprs, folds = 10, procs = 10 ):
    pool = mp.Pool( processes = procs )
    tmp = [pool.apply_async(create, args=( type, indices, classes, exprs, fold)) for fold in range (folds)]
    result = [p.get() for p in tmp]
    pool.terminate()
    result.sort()
    classifiers = [c[1] for c in result]
    return classifiers

def avgAccuracy ( classifiers, indices, classes, exprs, change, test, series, folds = 10, repeats = 10, procs = 10 ):
    pool = mp.Pool( processes = procs )
    tmp = [pool.apply_async( accuracy, args=( classifiers, indices, classes, exprs, change, test, series ) ) for r in range ( repeats ) ]
    result = [p.get() for p in tmp]
    pool.terminate()
    result = np.array(result)
    avg = sum (result) / repeats
    return avg