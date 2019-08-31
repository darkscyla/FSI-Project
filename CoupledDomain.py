from Matrix import Matrix
from Vector import Vector

import numpy as np

class CoupledDomain:

    def __init__(self, *domains):
        self.domainList = list(domains)

        self.size = sum([len(i.nodes) * i.dofs for i in self.domainList])
        self.totalConstraints = sum([len(i.constraintList) for i in self.domainList])

        self.stiffnessMatrix = Matrix(0)
        self.displacementVector = Vector(0)
        self.loadVector = Vector(0)

        self.couplingList = []
        self.couplingListRHS = []

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

    def __assembleDisplacementVector__(self):
        self.displacementVector = Vector(self.size)
        startPos = 0

        for domain in self.domainList:

            domainSize = len(domain.nodes) * domain.dofs

            for key, val in domain.constraintList.items():
                self.displacementVector[key + startPos] = val

            startPos += domainSize

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

    def addCouplingCondition(self, couplingArray, val):

        if len(couplingArray) % 2 is not 0 or len(couplingArray) is 0:
            print(f'Inconsistent Coupling Condition:{couplingArray}')
            return None

        self.couplingList.append(couplingArray)
        self.couplingListRHS.append(val)

    def solve(self):
        ''' Assemble all Matrices '''
        self.assemble()

        ''' Sub Matrix Assembly '''
        subMatrix = Matrix(self.size - self.totalConstraints)
        startPos = 0
        startPosGlob = 0
        startPosConstraints = self.size - len(self.couplingList) - self.totalConstraints

        for domain in self.domainList:

            unConstrainedList = [i for i in range(len(domain.nodes) * domain.dofs) if i not in domain.constraintList]

            for i in range(len(unConstrainedList)):
                for j in range(len(unConstrainedList)):
                    subMatrix[i + startPos][j + startPos] = domain.stiffnessMatrix[unConstrainedList[i]][unConstrainedList[j]]

            for i, coupling in enumerate(self.couplingList):
                for j in range(len(unConstrainedList)):
                    if coupling.get(unConstrainedList[j] + startPosGlob):
                        subMatrix[startPosConstraints + i][j + startPos] = coupling[unConstrainedList[j] + startPosGlob]
                        subMatrix[j + startPos][startPosConstraints + i] = coupling[unConstrainedList[j] + startPosGlob]

            startPos += len(unConstrainedList)
            startPosGlob += len(domain.nodes) * domain.dofs

        ''' General RHS computation '''
        subLoadVector = Vector(self.size - self.totalConstraints)
        startPos = 0

        for domain in self.domainList:

            unConstrainedList = [i for i in range(len(domain.nodes) * domain.dofs) if i not in domain.constraintList]
            constrainedListKeys = list(domain.constraintList.keys())
            constrainedListVals = list(domain.constraintList.values())

            for i, j in enumerate(unConstrainedList):
                if domain.loadList.get(j):
                    subLoadVector[i + startPos] = domain.loadList[j]

            for i in range(len(domain.constraintList)):
                for j in range(len(unConstrainedList)):
                    subLoadVector[j + startPos] -= \
                        constrainedListVals[i] * self.stiffnessMatrix[unConstrainedList[j], constrainedListKeys[i]]

            startPos += len(unConstrainedList)

        for i in range(len(self.couplingListRHS)):
            subLoadVector[startPosConstraints + i] = self.couplingListRHS[i]

        # np.savetxt('test.txt', subMatrix.matrix, delimiter=', ', fmt='%+1.2f')

        # print(subMatrix)
        # print(subLoadVector)

        return ~subMatrix * subLoadVector

    def assemble(self):
        self.size += len(self.couplingList)
        self.__assembleStiffnessMatrix__()
        self.__assembleDisplacementVector__()
        self.__assembleLoadVector__()
