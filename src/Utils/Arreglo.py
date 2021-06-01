class Arreglo():
    def __init__(self, name):
        self.name = name
        self.arrNodes = []
        # self.type = type
        # self.dim = dim
        # self.R = (self.lsDim - self.liDim + 1) * 1
        # self.arrNodes = []

    def addNode(self,liDim, lsDim):
        self.arrNodes.append(ArregloNodo(liDim, lsDim))
        return 0

    def clearArr(self):
        self.arrNodes = []

class ArregloNodo():
    R = 1
    def __init__(self, liDim, lsDim):
        self.type = type
        self.liDim = int(liDim.value)
        self.lsDim = int(lsDim.value)
        self.R = self.lsDim - self.liDim * self.R
        self.m = 0