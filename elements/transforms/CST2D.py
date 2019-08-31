import numpy as np

def CST2D(element, stiffnessMatrix):

	Node1 = element.getNode(0)
	Node2 = element.getNode(1)
	Node3 = element.getNode(2)

	dofsMap = [2 * Node1.id, 2 * Node1.id + 1,
			   2 * Node2.id, 2 * Node2.id + 1,
			   2 * Node3.id, 2 * Node3.id + 1]

	E = element.E
	v = element.poissonRatio
	t = element.thickness

	q1 = Node2.y - Node3.y
	q2 = Node3.y - Node1.y
	q3 = Node1.y - Node2.y

	r1 = Node3.x - Node2.x
	r2 = Node1.x - Node3.x
	r3 = Node2.x - Node1.x

	A = 0.5 * np.linalg.det(np.array([[1, Node1.x, Node1.y], 
									  [1, Node2.x, Node2.y],
									  [1, Node3.x, Node3.y]]))

	# B-Matrix
	B = 1 / 2 / A * np.array([[q1,  0, q2,  0, q3,  0],
				  			  [0,  r1,  0, r2,  0, r3],
				  			  [r1, q1, r2, q2, r3, q3]])
	
	# D-Matrix
	D = E / (1 - v**2) * np.array([[1, v, 0],
								   [v, 1, 0],
								   [0, 0, (1 - v)/2]])
	
	K = (np.transpose(B) @ D @ B ) * A * t


	# Global Stiffness Matrix Assembly
	for i in range(len(dofsMap)):
		for j in range(len(dofsMap)):
			stiffnessMatrix[dofsMap[i]][dofsMap[j]] += K[i][j]
