import numpy as np 

class Matrix():

    def __init__(self, n):
        if (isinstance(n, np.ndarray)):
            self.matrix = n
        else:
            self.matrix = np.zeros(shape=(n, n))

    def __repr__(self):
        return repr(self.matrix)
    
    def __mul__(self, other):
        return Matrix(np.matmul(self.matrix, other.matrix))

    def __getitem__(self, index):
        return self.matrix[index]

    def __invert__(self):
        return Matrix(np.linalg.inv(self.matrix))

    def inverse(self):
        return self.__invert__()

    def tolist(self):
        return self.matrix.tolist()