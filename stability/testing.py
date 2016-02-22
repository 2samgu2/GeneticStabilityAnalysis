"""testing.py.

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

import sys
import numpy as np
import multiprocessing as mp
import stability.multi as multi
import stability.serial as serial
from stability.fold import kFoldInd

"""
change == 0 --> greedy selection
change == 1 --> chi2 selection
change == 2 --> random selection
"""
def getAccuracy ( index, chosen, notChosen, series, size, type, change, flag = False, folds = 10, repeats = 10 ):

    if ( change == 0 ):
        test = [ i for i in chosen ]
        test.append( notChosen[ index ] )

    if ( change == 1 or change == 2 or change == 3 ):
        test = index

    classes = np.load ( "FAST/%s_classes.npy" % series )
    exprs = np.load ( "FAST/%s_%03d_fs_genes.npy" % ( series, size ) )

    training, testing = kFoldInd ( classes, folds )

    if (flag):
        classifiers = multi.getClassifiers( type, training, classes, exprs )
        avg = multi.avgAccuracy( classifiers, testing, classes, exprs, change, test, series )
    else :
        classifiers = serial.getClassifiers( type, training, classes, exprs )
        avg = serial.avgAccuracy( classifiers, testing, classes, exprs, change, test, series  )

    return index, avg

#serial multi greedy
def smgAccuracy ( chosen, notChosen, series, size, type, change, folds = 10, repeats = 10 ):
    result = [ getAccuracy( i, chosen, notChosen, series, size, type, change, flag = True ) for i in range ( len ( notChosen ) ) ]
    accuracy = [ a[1] for a in result ]
    return accuracy

#multi serial greedy
def msgAccuracy ( chosen, notChosen, series, size, type, change, folds = 10, repeats = 10 ):
    pool = mp.Pool( processes = mp.cpu_count() )
    tmp = [ pool.apply_async( getAccuracy, args=( i, chosen, notChosen, series, size, type, change ) ) for i in range ( len( notChosen ) ) ]
    result = [ p.get() for p in tmp ]
    pool.terminate()
    result.sort()
    accuracy = [ a[1] for a in result ]
    return accuracy

def greedy (series, size, type, change, folds = 10, repeats = 10):
    sys.stdout.write( "%s" % series )
    sys.stdout.write( "[%s]" % ( " " * size ) )
    sys.stdout.flush()
    sys.stdout.write( "\b" * ( size + 1 ) )

    genes = np.arange( 0, size, 1 )
    notChosen = genes.tolist()
    selected = []
    chosen = []

    for k in range( size ):
        accuracy = msgAccuracy ( chosen, notChosen, series, size, type, change )
        ol = [ ( k, v ) for k, v in zip( notChosen, accuracy ) ]
        ol.sort( key = lambda tup: tup[1] )
        chosen.append( ol[0][0] )
        selected.append( ol[0] )
        notChosen.remove( ol[0][0] )

        sys.stdout.write( "-" )
        sys.stdout.flush()

    sys.stdout.write("\n")

    return selected

#serial multi chi2 or rand
def smcrAccuracy ( sub_feats, series, size, type, change, folds = 10, repeats = 10 ):
    result = []
    for fs in sub_feats:
        result.append( getAccuracy( fs, None, None,
                                    series, size, type,
                                    change, flag = True ) )
        sys.stdout.write( "-" )
        sys.stdout.flush()
    accuracy = [ a[1] for a in result ]
    return accuracy

#multi serial chi2 or rand
def mscrAccuracy ( sub_feats, series, size, type, change, folds = 10, repeats = 10 ):
    pool = mp.Pool( processes = mp.cpu_count() )
    tmp = [ pool.apply_async( getAccuracy, args=( fs, None, None, series, size, type, change ) ) for fs in sub_feats ]
    result = [ p.get() for p in tmp ]
    pool.terminate()
    result.sort()
    for fs in sub_feats:
        sys.stdout.write( "-" )
        sys.stdout.flush()
    accuracy = [ a[1] for a in result ]
    return accuracy

def chi2rand (sub_feats, series, size, type, change, folds = 10, repeats = 10):
    sys.stdout.write( "%s" % series )
    sys.stdout.write( "[%s]" % ( " " * len(sub_feats) ) )
    sys.stdout.flush()
    sys.stdout.write( "\b" * ( len(sub_feats) + 1 ) )
    selected = mscrAccuracy( sub_feats, series, size, type, change )
    sys.stdout.write("\n")

    return selected
