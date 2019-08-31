def zeroD(element, stiffnessMatrix):

    i = element.getNode().id
    elementStiffness = element.getStiffness()

    stiffnessMatrix[i][i] += elementStiffness