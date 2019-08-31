from Domain import Domain
from CoupledDomain2 import CoupledDomain
from elements.transforms.oneD import oneD
from elements.Spring import Spring
from elements.NodeElement import NodeElement
from Plot import Plot
from solvers.Newmark import Newmark

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
structuralDomain.addNode(x = 0, y = 0)
structuralDomain.addNode(x = 5, y = 0, mass = 1)
structuralDomain.addNode(x = 10, y = 0, mass = 1)

###########               Elements               ###########
#----------------------------------------------------------#
'''
addElements(Element Type, (Node Tuple), Arguments of the element)
'''
structuralDomain.addElement(Spring, (0, 1), 10)
structuralDomain.addElement(NodeElement, (2,))      # Dummy mass element

###########      Assemble Stiffness matrix       ###########
#----------------------------------------------------------#
structuralDomain.assembleStiffnessMatrix()

###########            Add Constraints           ###########
#----------------------------------------------------------#
structuralDomain.addConstraint(0, 0)
structuralDomain.addLoads(1, 10)
structuralDomain.addLoads(2, 10)

###########           Coupled Domain            ###########
#----------------------------------------------------------#
coupledDomain = CoupledDomain(structuralDomain)
coupledDomain.addCouplingCondition({1: 1, 2: -1}, 0)

coupledDomain.Solve(Newmark, 10, .1, 1/4, 1/2)

plt.plot(coupledDomain.solver.history[0])
plt.plot(coupledDomain.solver.history[1])

plt.show()

# Plot(structuralDomain)

###########           Post Processing            ###########
#----------------------------------------------------------#
# Plot(structuralDomain)
