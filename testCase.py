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

###########               Elements               ###########
#----------------------------------------------------------#
'''
addElements(Element Type, (Nodes Tuple), Arguments of the element)
'''
structuralDomain.addElement(Spring, ( 0, 1 ), 975)
structuralDomain.addElement(Spring, ( 1, 2 ), 845)
structuralDomain.addElement(Spring, ( 2, 3 ), 715)
structuralDomain.addElement(Spring, ( 3, 4 ), 585)

###########      Assemble Stiffness matrix       ###########
#----------------------------------------------------------#
structuralDomain.assembleStiffnessMatrix()

###########            Add Constraints           ###########
#----------------------------------------------------------#
structuralDomain.addConstraint(0, 0)

structuralDomain.addLoads(1, 0)
structuralDomain.addLoads(2, 0)
structuralDomain.addLoads(3, 0)
structuralDomain.addLoads(4, 1)

###########           Coupled Domain            ###########
#----------------------------------------------------------#
coupledDomain = CoupledDomain(structuralDomain)
result = (coupledDomain.solve()).tolist()

print(f'Results from the FEM code: \t\t\t\t{np.around(result, decimals=6).transpose()}')
print(f'Expected result from Saeed Mavoni (Ex: 1.1): \t{[0.001026, 0.002210, 0.003608, 0.005317]}')

# Plot(structuralDomain)

###########           Post Processing            ###########
#----------------------------------------------------------#
# Plot(structuralDomain)
