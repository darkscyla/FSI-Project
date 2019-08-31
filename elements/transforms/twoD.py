from math import atan, cos, sin, pi

def twoD(element, stiffnessMatrix):

    i = 2 * element.getNode(0).id
    j = 2 * element.getNode(1).id

    x1 = element.getNode(0).x
    x2 = element.getNode(1).x

    y1 = element.getNode(0).y
    y2 = element.getNode(1).y

    elementStiffness = element.getStiffness()

    if x2 - x1 is 0:
        elementAngle = pi / 2
    else:
        elementAngle = atan((y2 - y1)/(x2 - x1))

    kC2 = elementStiffness * cos(elementAngle) * cos(elementAngle)
    kS2 = elementStiffness * sin(elementAngle) * sin(elementAngle)
    kCS = elementStiffness * cos(elementAngle) * sin(elementAngle)

    # cos(x) * cos(x)      cos(x) * sin(x)    _______\      NW | NE
    # cos(x) * sin(x)      sin(x) * sin(x)           /      SW | SE
    # NW:
    stiffnessMatrix[i][i]           +=  kC2
    stiffnessMatrix[i + 1][i]       +=  kCS
    stiffnessMatrix[i][i + 1]       +=  kCS
    stiffnessMatrix[i + 1][i + 1]   +=  kS2

    # SE:
    stiffnessMatrix[j][j]           +=  kC2
    stiffnessMatrix[j + 1][j]       +=  kCS
    stiffnessMatrix[j][j + 1]       +=  kCS
    stiffnessMatrix[j + 1][j + 1]   +=  kS2

    # NE:
    stiffnessMatrix[i][j]           -=  kC2
    stiffnessMatrix[i + 1][j]       -=  kCS
    stiffnessMatrix[i][j + 1]       -=  kCS
    stiffnessMatrix[i + 1][j + 1]   -=  kS2

    # SW:
    stiffnessMatrix[j][i]           -=  kC2
    stiffnessMatrix[j + 1][i]       -=  kCS
    stiffnessMatrix[j][i + 1]       -=  kCS
    stiffnessMatrix[j + 1][i + 1]   -=  kS2
