import timeit

mysetup  = '''

from Domain import Domain
from CoupledDomain2 import CoupledDomain
from elements.transforms.oneD import oneD
from elements.Spring import Spring
from elements.NodeElement import NodeElement
from Plot import Plot

import numpy as np

'''

mycode = '''

###########               Domains               ###########
#---------------------------------------------------------#
# Structure #
# Domain(transformationFunction, dofs per node)
structuralDomain = Domain( dim='2D')
# Fuild #
# fluidDomain = Domain()

###########                Nodes                 ###########
#----------------------------------------------------------#
# Structure #
structuralDomain.addNode(x=0, y=0)      # Node 0
structuralDomain.addNode(x=3, y=0)      # Node 1
structuralDomain.addNode(x=3, y=3)      # Node 2

###########               Elements               ###########
#----------------------------------------------------------#
# addElements(Element Type, (Nodes Tuple), Arguments of the element)

structuralDomain.addElement(Spring, ( 0, 1 ), 10)
structuralDomain.addElement(Spring, ( 1, 2 ), 5)
structuralDomain.addElement(Spring, ( 0, 2 ), 20)

###########      Assemble Stiffness matrix       ###########
#----------------------------------------------------------#
structuralDomain.assembleStiffnessMatrix()

###########            Add Constraints           ###########
#----------------------------------------------------------#
# addConstraints(Node, Value of displacement at node)

structuralDomain.addConstraint(0, 0)
structuralDomain.addConstraint(1, -.5)
structuralDomain.addConstraint(3, .4)

structuralDomain.addLoads(4, 2)
structuralDomain.addLoads(5, 1)

###########           Coupled Domain            ###########
#----------------------------------------------------------#
coupledDomain = CoupledDomain(structuralDomain)
result = (coupledDomain.solve()).tolist()
result = result[0:6]

loads = coupledDomain.loadVector[0:6]

# Plot(structuralDomain)

###########           Post Processing            ###########
#----------------------------------------------------------#
# Plot(structuralDomain)

'''

print(timeit.timeit(setup = mysetup, stmt = mycode, number = 10000))
