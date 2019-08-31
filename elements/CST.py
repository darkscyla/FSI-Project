from .Element import Element
from .transforms.CST2D import CST2D


class CST(Element):

    transformsMap = {'2D': CST2D}

    def __init__(self, nodesList, E, poissonRatio, thickness):
        super().__init__(nodesList)
        self.E = E
        self.poissonRatio = poissonRatio
        self.thickness = thickness

    def localStiffnessMatrix(self, dim, globalMatrix):
        '''
        Assembles the local stiffness matrix depending upon whether
        the problem is 1D, 2D, 3D

        dim             --->    dimension of the problem
        globalMatrix    --->    stiffness matrix
        '''
        CST.transformsMap[dim](self, globalMatrix)