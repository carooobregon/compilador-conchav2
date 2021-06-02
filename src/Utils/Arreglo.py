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
        self.size = self.size * dim
        self.arrNodes.append(dim)
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
    def __init__(self, name, elem, dim, baseMem, type, obj):
        self.obj = obj
        self.elem = self.parseElem(elem)
        self.type = type
        self.dim = dim
        self.name = name
        self.baseMem = baseMem
        self.memadd  = self.calculateMemAddress()

    def parseElem(self, p):
        r = []
        if isinstance(p, int):
            return p
        for i in p:
            r.append(int(i))
        return r
        
    def calculateMemAddress(self):
        if self.dim == 1:
            return self.baseMem + self.elem
        elif self.dim == 2:
            return self.baseMem + self.elem[0] * self.obj.arrNodes[1] + self.elem[1]

    # def validateObjDim(self):
        