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
structuralDomain = Domain( dim='2D')
structuralDomain2 = Domain( dim='2D')
''' Fuild '''
# fluidDomain = Domain()

###########                Nodes                 ###########
#----------------------------------------------------------#
''' Structure '''
structuralDomain.addNode(x=0, y=0)      # Node 0
structuralDomain.addNode(x=3, y=0)      # Node 1
structuralDomain.addNode(x=0, y=3)      # Node 2
structuralDomain.addNode(x=3, y=3)      # Node 3
structuralDomain.addNode(x=6, y=3)      # Node 4

structuralDomain2.addNode(x=3, y=0)     # Node 0
structuralDomain2.addNode(x=6, y=3)     # Node 1

###########               Elements               ###########
#----------------------------------------------------------#
'''
addElements(Element Type, (Nodes Tuple), Arguments of the element)
'''
structuralDomain.addElement(Spring, ( 0, 1 ), 4.22 * 1e5 )
structuralDomain.addElement(Spring, ( 1, 2 ), 2.98 * 1e5 )
structuralDomain.addElement(Spring, ( 2, 3 ), 4.22 * 1e5 )
structuralDomain.addElement(Spring, ( 1, 3 ), 4.22 * 1e5 )
structuralDomain.addElement(Spring, ( 3, 4 ), 4.22 * 1e5 )

structuralDomain2.addElement(Spring, ( 0, 1 ), 2.98 * 1e5 )

###########      Assemble Stiffness matrix       ###########
#----------------------------------------------------------#
structuralDomain.assembleStiffnessMatrix()
structuralDomain2.assembleStiffnessMatrix()

###########            Add Constraints           ###########
#----------------------------------------------------------#
'''
addConstraints(Node, Value of displacement at node)
'''
structuralDomain.addConstraint(0, 0)
structuralDomain.addConstraint(1, 0)
structuralDomain.addConstraint(4, 0)
structuralDomain.addConstraint(5, 0)

structuralDomain.addLoads(7, -500)
structuralDomain.addLoads(9, -500)

###########           Coupled Domain            ###########
#----------------------------------------------------------#
coupledDomain = CoupledDomain(structuralDomain, structuralDomain2)

coupledDomain.addCouplingCondition({2:1, 10:-1}, 0)
coupledDomain.addCouplingCondition({3:1, 11:-1}, 0)
coupledDomain.addCouplingCondition({8:1, 12:-1}, 0)
coupledDomain.addCouplingCondition({9:1, 13:-1}, 0)

result = (coupledDomain.solve()).tolist()

# Delete extra entries that come from coupling
for i in range(8):
    del result[-1]

print(f'Results from the FEM code: \t\t\t\t{np.around(result, decimals=6).transpose()}')
print(f'Expected result from Saeed Moaveni (Ex: 3.1): \t{[-0.00355, -0.01026, 0.00118, -0.0114, 0.0024, -0.0195]}')

# Plot(structuralDomain)

###########           Post Processing            ###########
#----------------------------------------------------------#
# Plot(structuralDomain)
