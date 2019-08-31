from Domain import Domain
from CoupledDomain import CoupledDomain
from elements.transforms.oneD import oneD
from elements.Spring import Spring
from elements.NodeElement import NodeElement
from Plot import Plot

import numpy as np

###########               Domains               ###########
#---------------------------------------------------------#
''' Structure '''
# Domain(transformationFunction, dofs per node)
structuralDomain = Domain( dim='1D')
''' Fuild '''
# fluidDomain = Domain()

###########                Nodes                 ###########
#----------------------------------------------------------#
''' Structure '''
structuralDomain.addNode(0)
structuralDomain.addNode(1)
structuralDomain.addNode(2)
structuralDomain.addNode(3)
structuralDomain.addNode(4)
structuralDomain.addNode(5)
structuralDomain.addNode(6)

###########               Elements               ###########
#----------------------------------------------------------#
'''
addElements(Element Type, (Nodes Tuple), Arguments of the element)
'''
structuralDomain.addElement(Spring, ( 0, 1 ), 100)
structuralDomain.addElement(Spring, ( 1, 2 ), 100)
structuralDomain.addElement(Spring, ( 2, 3 ), 100)
structuralDomain.addElement(Spring, ( 3, 4 ), 100)
structuralDomain.addElement(Spring, ( 4, 5 ), 100)
structuralDomain.addElement(Spring, ( 5, 6 ), 100)

###########      Assemble Stiffness matrix       ###########
#----------------------------------------------------------#
structuralDomain.assembleStiffnessMatrix()

###########            Add Constraints           ###########
#----------------------------------------------------------#
structuralDomain.addConstraint(0, 0)

structuralDomain.addLoads(0, 1)
structuralDomain.addLoads(1, 2)
structuralDomain.addLoads(2, 3)
structuralDomain.addLoads(3, 4)
structuralDomain.addLoads(4, 5)
structuralDomain.addLoads(5, 6)
structuralDomain.addLoads(6, 7)

###########           Coupled Domain            ###########
#----------------------------------------------------------#
coupledDomain = CoupledDomain(structuralDomain)

coupledDomain.addCouplingCondition({1: 1, 5: -1}, 1/5)

result = (coupledDomain.solve()).tolist()
del result[-1]

print(f'Results from the FEM code: \t\t\t\t{np.around(result, decimals=6).transpose()}')
print(f'Expected result from Filipa (Ex: 9.1): \t{[0.27, 0.275, 0.25, 0.185, 0.070, 0.14]}')

# Plot(structuralDomain)

###########           Post Processing            ###########
#----------------------------------------------------------#
# Plot(structuralDomain)
