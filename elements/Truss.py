from .Element import Element
from .transforms.oneD import oneD
from .transforms.twoD import twoD


class Spring(Element):

    transformsMap = {'1D': oneD, '2D': twoD}

    def __init__(self, nodesList, E, A):
        super().__init__(nodesList)         # Store the nodes list
        self.E = E
        self.A = A
        self.L = self.getLength()

    def getStiffness(self):
        '''
        Returns the stiffness of the element
        '''
        return self.E * self.A / self.L

    def getLength(self):
        Node1 = self.nodesList[0]
        Node2 = self.nodesList[1]

        length = ((Node1.x - Node2.x)**2 + (Node1.y - Node2.y)**2 + (Node1.z - Node2.z)**2)**.5

        return length

    def localStiffnessMatrix(self, dim, globalMatrix):
        '''
        Assembles the local stiffness matrix depending upon whether
        the problem is 1D, 2D, 3D

        dim             --->    dimension of the problem
        globalMatrix    --->    stiffness matrix
        '''
        Spring.transformsMap[dim](self, globalMatrix)