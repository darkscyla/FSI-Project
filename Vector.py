import numpy as np


class Vector():

    def __init__(self, n):
        if (isinstance(n, np.ndarray)):
            self.matrix = n
        else:
            self.matrix = np.zeros(shape=(n, 1))

    def __repr__(self):
        return repr(self.matrix)

    def __getitem__(self, index):
        return self.matrix[index]

    def __setitem__(self, index, value):
        self.matrix[index] = value

    def __add__(self, other):
    	return Vector(self.matrix + other.matrix)