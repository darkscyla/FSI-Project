from .Element import Element
from .transforms.oneD import oneD
from .transforms.twoD import twoD


class Spring(Element):

    transformsMap = {'1D': oneD, '2D': twoD}

    def __init__(self, nodesList, stiffness):
        super().__init__(nodesList)
        self.stiffness = stiffness

    def getStiffness(self):
        '''
        Returns the stiffness of the element
        '''
        return self.stiffness

    def localStiffnessMatrix(self, dim, globalMatrix):
        '''
        Assembles the local stiffness matrix depending upon whether
        the problem is 1D, 2D, 3D

        dim             --->    dimension of the problem
        globalMatrix    --->    stiffness matrix
        '''
        Spring.transformsMap[dim](self, globalMatrix)