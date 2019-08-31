import matplotlib.pyplot as plt

def Plot(Structure):
    xArray = []
    yArray = []

    for i in Structure.elements:

        if i.isPlotable():
            xArray.append(i.getNode(0).x)
            xArray.append(i.getNode(1).x)

            yArray.append(i.getNode(0).y)
            yArray.append(i.getNode(1).y)

    plt.plot(xArray, yArray, '-ro')
    plt.gca().set_aspect('equal', 'datalim')
    plt.show()