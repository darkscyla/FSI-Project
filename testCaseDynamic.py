from Domain import Domain
from CoupledDomain2 import CoupledDomain
from elements.transforms.oneD import oneD
from elements.Spring import Spring
from elements.NodeElement import NodeElement
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
structuralDomain.addNode(0, 0)
structuralDomain.addNode(5, 0, 2)
structuralDomain.addNode(10, 0, 1)
structuralDomain.addNode(15, 0)


###########               Elements               ###########
#----------------------------------------------------------#
'''
addElement(Element Type, NodeTuple, Arguments of the element)
'''
structuralDomain.addElement(Spring, (0, 1), 4)
structuralDomain.addElement(Spring, (1, 2), 2)
structuralDomain.addElement(Spring, (2, 3), 2)

###########      Assemble Stiffness matrix       ###########
#----------------------------------------------------------#
structuralDomain.assembleStiffnessMatrix()

###########            Add Constraints           ###########
#----------------------------------------------------------#
structuralDomain.addConstraint(0, 0)
structuralDomain.addConstraint(3, 0)
structuralDomain.addLoads(2, 10)

###########           Coupled Domain            ###########
#----------------------------------------------------------#
coupledDomain = CoupledDomain(structuralDomain)
coupledDomain.addPhysics(gravity=0)

coupledDomain.Solve(Newmark, 10, 0.01, 1/4, 1/2)

###########           Post Processing            ###########
#----------------------------------------------------------#
# Settings
plt.grid(color='#7f7f7f', linestyle='-', linewidth = '.1')

plt.plot(coupledDomain.solver.time, coupledDomain.solver.history[0], label='Mass 1')
plt.plot(coupledDomain.solver.time, coupledDomain.solver.history[1], label='Mass 2')
plt.legend(loc='upper right', fontsize=14)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.title('Displacement over time', fontsize=24)
plt.xlabel('Time (sec)', fontsize=18)
plt.ylabel('Displacement (m)', fontsize=18)

plt.show()
# Plot(structuralDomain)

###########           Post Processing            ###########
#----------------------------------------------------------#
# Plot(structuralDomain)
