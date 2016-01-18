import numpy as np
from collections import Counter
from sklearn.metrics import mean_squared_error
from scipy.sparse.linalg import lsqr
from math import sqrt

class Model:
    
    def __init__(self, samples, eps, class_label):
        
        self.class_label = class_label
        self.samples = np.array(samples)
        self.eps = eps
        
        self.correlation = np.corrcoef( self.samples, y=None, rowvar=0, bias=0, ddof=None ) # columns are variables, rows are samples
        
        self.mask = (np.absolute(self.correlation) > self.eps) # note that the mask is actually the graph
        
        self.geneFuncMasks = [] #these are the coefficients in Ax=b
        for gene in range(len(self.correlation)):
            currMask = self.mask[gene]
            setOfNeighbors = []
            solutions = []
            for sample in self.samples:
                neighbors = [sample[neighbor] if ((currMask[neighbor] == True) and (gene != neighbor)) else 0 for neighbor in range(len(currMask))]
                neighbors.append(1)
                setOfNeighbors.append(neighbors)
                solutions.append(sample[gene])
            coeff = self.AxbSolver(setOfNeighbors, solutions, 2)
            self.geneFuncMasks.append(coeff.tolist())
        
        self.coefficients = np.array(self.geneFuncMasks)
    
    def AxbSolver(self, neighbors, sols, choice):
        # Use lsqr to solve Ax=b
        A=np.array(neighbors)
        b=np.array(sols)
        x = lsqr(A,b)[0]
        return x
    
    def getExpression(self, sample):
        expression = []
        for gene in range(len(self.coefficients)):
            geneVal = 0
            for neighbor in range(len(self.mask)-1):
                geneVal += self.coefficients[gene][neighbor] * sample[neighbor]
            geneVal += self.coefficients[gene][len(self.mask)]
            expression.append(geneVal)
        return np.array(expression)
    
    def getClass (self):
        return self.class_label

class NetworkBasedClassifier:
    
    def __init__(self, epsilon):
        
        self.models = []
        self.epsilon = epsilon
    
    def fit ( self, X, y ):
        y = np.array(y)
        X = np.array(X)
        for key in Counter( y ):
            a_class = np.where( y == key )
            self.models.append( Model ( [ X[i] for i in a_class[0] ], self.epsilon, key  ) )
    
    def predict ( self, X ):
        classifications = []
        for sample in X:
            RMSEs = []
            for model in self.models:
                rmse = sqrt( mean_squared_error( sample, model.getExpression( sample ) ) )
                RMSEs.append(rmse)
            min_index = RMSEs.index( min(RMSEs) )
            label = self.models[min_index].getClass()
            classifications.append(label)
        return np.array(classifications)
