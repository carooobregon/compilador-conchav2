class Arreglo():
    def __init__(self, name):
        self.name = name
        self.arrNodes = []
        self.currR = 1
        self.memAddress = 0
        # self.type = type
        # self.dim = dim
        # self.R = (self.lsDim - self.liDim + 1) * 1
        # self.arrNodes = []

    def addNode(self,liDim, lsDim):
        liDim = int(liDim.value)
        lsDim = int(lsDim.value)
        self.arrNodes.append(ArregloNodo(liDim, lsDim, self.currR))
        self.currR = ( lsDim - liDim  + 1 ) * self.currR
        return 0
    
    def processArray(self):
        self.processLastElem()
        return

    def processLastElem(self):
        offset = self.arrNodes[-1].liDim * 1
        self.arrNodes[-1].setM(offset * -1)

    def clearArr(self):
        self.arrNodes = []

class ArregloNodo():
    def __init__(self, liDim, lsDim, pastR):
        self.type = type
        self.liDim = liDim
        self.lsDim = lsDim
        self.R = (self.lsDim - self.liDim) * pastR
        self.m = 0
    
    def setM(self, val):
        self.m = val