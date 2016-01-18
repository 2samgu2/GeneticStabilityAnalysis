import numpy as np
from random import uniform

def getChange ( str ):
    changes = [ "greedy", "chi2", "rand", "percent" ]
    return changes.index( str.lower() )

def all ( exprs, percent ):
    result = []
    for expr in exprs:
        alt = []
        for g in expr:
            off = g * percent
            low = g - off
            high = g + off
            alt.append( uniform( low, high ) )
        result.append( alt )
    return np.array( result )

def get_rand_expressions ( exps ):
    high = np.amax( exps )
    low = np.amin( exps )
    rand_exps = []
    for exp in exps:
        new_exp = []
        for gene in exp:
            new_exp.append( uniform( low, high ) )
        rand_exps.append( new_exp )
    return np.array(rand_exps)

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

def subset ( exprs, indices, series, change ):
    high = np.amax( exprs )
    low = np.amin( exprs )
    
    # NOTE: indices in the file refers to the num of features being selected
    if ( change == 1 ):
        file = ( "FASTR/%s_%03d_%03d_nCk.npy" % ( series, len( exprs[0] ), indices) )
        indices = np.load( file )
    elif ( change == 2 ):
        file = ( "FASTR/%s_%03d_%03d_nCk_rand.npy" % ( series, len( exprs[0] ), indices) )
        indices = np.load( file )

    result = []
    for exp in exprs:
        alt = [g for g in exp]
        for i in indices:
            alt[i] = uniform( low, high )
        result.append( alt )
    return np.array(result)