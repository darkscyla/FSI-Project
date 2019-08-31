from Domain import Domain
from CoupledDomain import CoupledDomain
from elements.transforms.oneD import oneD
from elements.CST import CST
from elements.NodeElement import NodeElement
from solvers.Newmark import Newmark
from loads.timeLoad import timeLoad

import matplotlib.pyplot as plt
import numpy as np

###########               Domains               ###########
#---------------------------------------------------------#
''' Structure '''
# Domain(transformationFunction, dofs per node)
structuralDomain = Domain(dim='2D')
''' Fuild '''
# fluidDomain = Domain()

###########                Nodes                 ###########
#----------------------------------------------------------#
''' Structure '''
structuralDomain.addNode(x=3, y=0)
structuralDomain.addNode(x=3, y=2)
structuralDomain.addNode(x=0, y=2)
structuralDomain.addNode(x=0, y=0)

###########               Elements               ###########
#----------------------------------------------------------#
'''
addElement(Element Type, NodeTuple, Arguments of the element)
'''
# CST( nodesTuple, elasticModulus, poissonsRatio, thickness)
structuralDomain.addElement(CST, (0, 1, 3), 30e6, 0.25, 0.5)
structuralDomain.addElement(CST, (2, 3, 1), 30e6, 0.25, 0.5)

###########      Assemble Stiffness matrix       ###########
#----------------------------------------------------------#
structuralDomain.assembleStiffnessMatrix()

###########            Add Constraints           ###########
#----------------------------------------------------------#
structuralDomain.addConstraint(1, 0)
structuralDomain.addConstraint(4, 0)
structuralDomain.addConstraint(5, 0)
structuralDomain.addConstraint(6, 0)
structuralDomain.addConstraint(7, 0)

# Loads
structuralDomain.addLoads(3, -1000)

# ###########           Coupled Domain            ###########
# #----------------------------------------------------------#
coupledDomain = CoupledDomain(structuralDomain)
print(coupledDomain.solve())

# coupledDomain.Solve(Newmark, 10, 0.01, 1/4, 1/2)

# ###########           Post Processing            ###########
# #----------------------------------------------------------#
# # Settings
# plt.grid(color='#7f7f7f', linestyle='-', linewidth = '.1')

# plt.plot(coupledDomain.solver.time, coupledDomain.solver.history[0], label='Mass 1')
# plt.plot(coupledDomain.solver.time, coupledDomain.solver.history[1], label='Mass 2')
# plt.legend(loc='upper right', fontsize=14)

# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)

# plt.title('Displacement over time', fontsize=24)
# plt.xlabel('Time (sec)', fontsize=18)
# plt.ylabel('Displacement (m)', fontsize=18)

# plt.show()
# Plot(structuralDomain)

###########           Post Processing            ###########
#----------------------------------------------------------#
# Plot(structuralDomain)
