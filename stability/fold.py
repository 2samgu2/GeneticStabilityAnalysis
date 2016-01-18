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