from .Vector import Vector
from .Matrix import Matrix

from copy import deepcopy

class Newmark():

    def __init__(self, coupledDomain, finalTime, dt, beta, gamma, lhsConstant = False):
        self.coupledDomain = coupledDomain
        self.size = self.coupledDomain.size
        self.finalTime = finalTime
        self.dt = dt
        self.beta = beta
        self.gamma = gamma
        self.lhsConstant = lhsConstant

        # Variables for history
        self.unew = Vector(self.size)
        self.u = Vector(self.size)

        self.vnew = Vector(self.size)
        self.v = Vector(self.size)

        self.anew = Vector(self.size)
        self.a = Vector(self.size)

        self.initialLoadVector = Vector(self.size)

        self.history = [[], []]
        self.time = []

        # Newmark coefficients
        self.a0 = 1 / self.beta / (self.dt ** 2)
        self.a1 = self.gamma / self.beta / self.dt
        self.a2 = 1 / self.beta / self.dt
        self.a3 = 1 / (2 * self.beta) - 1
        self.a4 = self.gamma / self.beta - 1
        self.a5 = self.dt / 2 * (self.gamma / self.beta - 2)
        self.a6 = self.dt * (1 - self.gamma)
        self.a7 = self.gamma * self.dt 

    def solve(self):

        # Copy initial load Vector
        self.initialLoadVector = deepcopy(self.coupledDomain.loadVector)


        for key, val in self.coupledDomain.ivDisplacementList.items():
            self.u[key] = val

        # Find acceleration from the initial conditions
        #---------------------------------------------------------------------------------------
        startPos = 0

        KxU = self.coupledDomain.stiffnessMatrix * (self.coupledDomain.displacementVector + self.u)

        for domain in self.coupledDomain.domainList:

            for i in range(len(domain.nodes)):
                
                currentPos = i + startPos

                self.a[currentPos] = self.coupledDomain.loadVector[currentPos] - KxU[currentPos]

            startPos += len(domain.nodes)

        startPos = 0

        for domain in self.coupledDomain.domainList:

            for i in range(len(domain.nodes)):
                
                currentPos = i + startPos

                mass = domain.nodes[i].mass

                if mass is not None:
                    self.a[currentPos] /= mass
                # else:
                #     print(f"CHECK: Expected 0, got {self.a[currentPos]}")

            startPos += len(domain.nodes)

        # Mass and Damping Matrix contributions to Stiffness Matrix
        #---------------------------------------------------------------------------------------
        startPos = 0

        for domain in self.coupledDomain.domainList:

            for i in range(len(domain.nodes)):
                
                currentPos = i + startPos

                mass = domain.nodes[i].mass
                damping = 0

                if mass is None:
                    mass = 0

                if currentPos in self.coupledDomain.dampingList.keys():
                    damping = self.coupledDomain.dampingList[currentPos]

                massLhsContribution = mass * self.a0
                dampingLhsContribution = damping * self.a1

                # Stiffness Matrix Update
                self.coupledDomain.stiffnessMatrix[currentPos][currentPos] += massLhsContribution + dampingLhsContribution

            startPos += len(domain.nodes)

        # Loop for time
        time = 0

        while ( time < self.finalTime):
            
            startPos = 0

            # Load Update at every time step
            for domain in self.coupledDomain.domainList:

                for key, loadFunctor in domain.loadFunctorList.items():

                    self.initialLoadVector[key + startPos] = loadFunctor(time)

                startPos += len(domain.nodes)

            startPos = 0

            # RHS Update at every time step
            for domain in self.coupledDomain.domainList:

                for i in range(len(domain.nodes)):
                    
                    currentPos = i + startPos

                    mass = domain.nodes[i].mass
                    damping = 0

                    if mass is None:
                        mass = 0
                    
                    if currentPos in self.coupledDomain.dampingList.keys():
                        damping = self.coupledDomain.dampingList[currentPos]

                    massRhsContribution = mass * ( self.a0 * self.u[currentPos]
                                                    + self.a2 * self.v[currentPos]
                                                    + self.a3 * self.a[currentPos])

                    dampingRhsContribution = damping * ( self.a1 * self.u[currentPos]
                                                          + self.a4 * self.v[currentPos]
                                                          + self.a5 * self.a[currentPos])
                     
                    # RHS update
                    self.coupledDomain.loadVector[currentPos] = self.initialLoadVector[currentPos] \
                                                                + massRhsContribution + dampingRhsContribution

                startPos += len(domain.nodes)

            # Solve the KU = F to get new U and F
            self.coupledDomain.__solve__(self.lhsConstant)
            self.unew = deepcopy(self.coupledDomain.displacementVector)

            ## Update Acceleration and Velocities
            startPos = 0

            for domain in self.coupledDomain.domainList:

                for i in range(len(domain.nodes)):

                    currentPos = i + startPos

                    self.anew[currentPos] = self.a0 * (self.unew[currentPos] - self.u[currentPos]) \
                                            - self.a2 * self.v[currentPos] \
                                            - self.a3 * self.a[currentPos]

                    self.vnew[currentPos] = self.v[currentPos] + self.a6 * self.a[currentPos] \
                                            + self.a7 * self.anew[currentPos]

                startPos += len(domain.nodes)

            self.u = deepcopy(self.unew)
            self.v = deepcopy(self.vnew)
            self.a = deepcopy(self.anew)

            self.history[0].append(self.coupledDomain.displacementVector[1])
            # self.history[1].append(self.initialLoadVector[1][0])
            self.history[1].append(self.coupledDomain.displacementVector[2])

            self.time.append(time)

            time += self.dt