class Arreglo():
    def __init__(self, name):
        self.name = name
        self.arrNodes = []
        self.currR = 1
        self.memAddress = 0
        self.size = 1
        # self.type = type
        # self.dim = dim
        # self.R = (self.lsDim - self.liDim + 1) * 1
        # self.arrNodes = []

    def addNode(self, dim):
        self.size = self.size * dim;
        return 0
    
    def processArray(self):            
        self.processLastElem()
        return

    def processLastElem(self):
        self.arrNodes[-1].setOffset(1)        
        self.arrNodes[-1].setK()

    def clearArr(self):
        self.arrNodes = []

class ArregloNodo():
    def __init__(self, name, elem, dim, baseMem, type):
        self.elem = int(elem)
        self.type = type
        self.dim = dim
        self.name = name
        self.baseMem = baseMem
        self.memadd  = self.calculateMemAddress()

    def calculateMemAddress(self):
        if self.dim == 1:
            return self.baseMem + self.elem

    def setK(self, val):
        self.m = self.liDim * -1

    def setOffset(self, val):
        self.offset = self.liDim * val