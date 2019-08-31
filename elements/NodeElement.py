from .Element import Element
from .transforms.zeroD import zeroD


class NodeElement(Element):

    def __init__(self, node):
        self.node = node

    def getNode(self):
        return self.node[0]

    def isPlotable(self):
        return False

    def getStiffness(self):
        '''
        Returns the stiffness of the element
        '''
        return 0

    def localStiffnessMatrix(self, dim, globalMatrix):
        '''
        Assembles the local stiffness matrix depending upon whether
        the problem is 1D, 2D, 3D

        dim             --->    dimension of the problem. This element dicards it
        globalMatrix    --->    stiffness matrix
        '''
        zeroD(self, globalMatrix)