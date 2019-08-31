from Matrix import Matrix
from Vector import Vector

import numpy as np

class CoupledDomain:

    def __init__(self, *domains):
        self.domainList = list(domains)

        self.size = sum([len(i.nodes) * i.dofs for i in self.domainList])
        self.dofs = self.size
        self.totalConstraints = sum([len(i.constraintList) for i in self.domainList])

        self.physics = {'gravity':0}

        self.stiffnessMatrix = Matrix(0)
        self.stiffnessMatrixInverse = Matrix(0)
        self.displacementVector = Vector(0)
        self.loadVector = Vector(0)

        self.solver = None
        self.inverseFlag = True

        self.couplingList = []
        self.couplingListRHS = []

        self.dampingList = {}
        self.ivDisplacementList = {}

        self.__assembleConstraints__()

    def __assembleStiffnessMatrix__(self):
        self.stiffnessMatrix = Matrix(self.size)
        startPos = 0

        ''' Stiffness Matrix contributions from Domains '''
        for domain in self.domainList:

            domainSize = len(domain.nodes) * domain.dofs

            for i in range(domainSize):
                for j in range(domainSize):
                    self.stiffnessMatrix[i + startPos][j + startPos] = domain.stiffnessMatrix[i][j]
            
            startPos += domainSize

        ''' Stiffness Matrix contributions from Couplings '''
        for coupling in self.couplingList:
            for key, val in coupling.items():
                self.stiffnessMatrix[startPos][key] = val
                self.stiffnessMatrix[key][startPos] = val

            startPos += 1

    def __assembleLoadVector__(self):
        self.loadVector = Vector(self.size)
        startPos = 0

        for domain in self.domainList:

            domainSize = len(domain.nodes) * domain.dofs

            for key, val in domain.loadList.items():
                self.loadVector[key + startPos] = val

            startPos += domainSize

        for couplingRHS in self.couplingListRHS:
            self.loadVector[startPos] = couplingRHS
            startPos += 1

        startPos = 0

        for domain in self.domainList:
             for i in domain.nodes:
                if i.mass is not None:
                    self.loadVector[startPos] += i.mass * self.physics['gravity']
                startPos += 1

    def __assembleConstraints__(self):
        startPos = 0

        for domain in self.domainList:

            for key, val in domain.constraintList.items():
                self.couplingList.append({key + startPos:1})
                self.couplingListRHS.append(val)
            
        startPos += len(domain.nodes) * domain.dofs

    def addCouplingCondition(self, couplingArray, val):
        self.couplingList.append(couplingArray)
        self.couplingListRHS.append(val)

    def __solve__(self, LHSConstant = False):

        if not LHSConstant:
            self.displacementVector = ~self.stiffnessMatrix * self.loadVector
        else:
            if self.inverseFlag:
                self.stiffnessMatrixInverse = ~self.stiffnessMatrix
                self.inverseFlag = False
            
            self.displacementVector = self.stiffnessMatrixInverse * self.loadVector

        # constraintsStartPos =  self.size - len(self.couplingList)

        '''
        # Assign values to load vector (Reaction forces)
        for i in range(self.totalConstraints):
            # Index corresponds to the DOF id
            # Put loads from lagrange to corresponding DOF
            index = list(self.couplingList[i].keys())[0]
            self.loadVector[index] = -self.displacementVector[constraintsStartPos + i]
        '''

    def __assemble__(self):
        self.size += len(self.couplingList)

        self.displacementVector = Vector(self.size)
       
        self.__assembleStiffnessMatrix__()
        self.__assembleLoadVector__()
    
    def Solve(self, Solver, *args):
        ''' Assemble all Matrices '''
        self.__assemble__()

        self.solver = Solver(self, *args)

        self.solver.solve()

    def addPhysics(self, **kwargs):
        for key, value in kwargs.items():
            self.physics[key] = value

    def addDamping(self, dampingList):
        self.dampingList = dampingList

    def addIVDisplacement(self, ivList):
        self.ivDisplacementList = ivList
