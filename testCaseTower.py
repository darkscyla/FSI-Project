from Domain2 import Domain
from CoupledDomain2 import CoupledDomain
from elements.transforms.oneD import oneD
from elements.Spring import Spring
from elements.NodeElement import NodeElement
from solvers.Newmark import Newmark
from loads.timeLoad import timeLoad

import matplotlib.pyplot as plt

###########               Domains               ###########
#---------------------------------------------------------#
''' Structure '''
# Domain(transformationFunction, dofs per node)
structuralDomain = Domain(dim='1D')
''' Fuild '''
# fluidDomain = Domain()

###########                Nodes                 ###########
#----------------------------------------------------------#
''' Structure '''
structuralDomain.addNode(0, 0)
structuralDomain.addNode(5, 0, 1)
# structuralDomain.addNode(10, 0, 1)

###########               Elements               ###########
#----------------------------------------------------------#
'''
addElements(Element Type, Node1, Node2, Arguments of the element)
'''
structuralDomain.addElement(Spring, (0, 1), 40)
# structuralDomain.addElement(NodeElement, (2,))

###########      Assemble Stiffness matrix       ###########
#----------------------------------------------------------#
structuralDomain.assembleStiffnessMatrix()

###########            Add Constraints           ###########
#----------------------------------------------------------#
structuralDomain.addConstraint(0, 0)
structuralDomain.addLoads(1, timeLoad)
# structuralDomain.addLoads(2, 7.62)

###########           Coupled Domain            ###########
#----------------------------------------------------------#
coupledDomain = CoupledDomain(structuralDomain)
coupledDomain.addPhysics(gravity=-9.81)
# coupledDomain.addCouplingCondition({1: 1, 2: -1}, 0)
coupledDomain.addDamping({1: 12.64911})

coupledDomain.Solve(Newmark, 10, .01, 1/4, 1/2)

plt.plot(coupledDomain.solver.time, coupledDomain.solver.history[0])
# plt.plot(coupledDomain.solver.time, coupledDomain.solver.history[1])
# plt.plot(coupledDomain.solver.history[1])
plt.show()
# Plot(structuralDomain)

###########           Post Processing            ###########
#----------------------------------------------------------#
# Plot(structuralDomain)
