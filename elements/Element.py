from abc import ABC, abstractmethod


class Element(ABC):

    def __init__(self, nodesList):
        self.nodesList = nodesList
        super().__init__()

    def getNode(self, key):
        return self.nodesList[key]

    def isPlotable(self):
        return True

    def getStiffness(self):
        pass

    @abstractmethod
    def localStiffnessMatrix(self, dim, globalMatrix):
        pass
