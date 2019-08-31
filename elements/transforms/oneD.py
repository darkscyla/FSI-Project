def oneD(element, stiffnessMatrix):

    i = element.getNode(0).id
    j = element.getNode(1).id
    elementStiffness = element.getStiffness()

    stiffnessMatrix[i][i] += elementStiffness
    stiffnessMatrix[j][j] += elementStiffness

    stiffnessMatrix[i][j] -= elementStiffness
    stiffnessMatrix[j][i] -= elementStiffness