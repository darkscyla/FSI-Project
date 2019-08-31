from Node import Node
from Matrix import Matrix


class Domain():

    dofsMap = {'1D': 1, '2D': 2, '3D': 3}

    def __init__(self, dim):
        ''' Dim     --- >   corresponds to diamension of the problem,
                            1D - 2D - 3D. This key word is used to
                            determine dofs from dofsMap and passed on
                            to the elements as a hint to correctly determine
                            the stiffness matrix transformation
        '''
        self.dim = dim
        self.dofs = Domain.dofsMap[dim]
        self.nodes = []
        self.elements = []
        self.stiffnessMatrix = Matrix(0)
        self.constraintList = {}
        self.loadList = {}
        self.loadFunctorList = {}

    def addNode(self, x, y=0, mass=None):
        id = len(self.nodes)
        self.nodes.append(Node(id, x, y, mass))

    def addElement(self, ElementType, nodesIDTuple, *args):
        nodesList = [self.nodes[i] for i in nodesIDTuple]
        self.elements.append(ElementType(nodesList, *args))

    def assembleStiffnessMatrix(self):
        self.stiffnessMatrix = Matrix(self.dofs * len(self.nodes))

        for element in self.elements:
            element.localStiffnessMatrix(self.dim, self.stiffnessMatrix)

        return self.stiffnessMatrix

    def addConstraint(self, node, val):
        self.constraintList[node] = val

    def addLoads(self, node, val):
        # Check if val is a function handle
        if callable(val):
            self.loadFunctorList[node] = val
            self.loadList[node] = val(0)
        else:
            self.loadList[node] = val