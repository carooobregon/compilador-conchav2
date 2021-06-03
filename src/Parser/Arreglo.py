# Class 'Array' that creates objects with the atributes name, dimensions of nodes, size, and base address

class Arreglo():
    def __init__(self, name):
        self.name = name
        self.arrNodes = []
        self.currR = 1
        self.memAddress = 0
        self.size = 1

    # Adds new dimension node to array
    def addNode(self, dim):
        self.size = self.size * dim
        self.arrNodes.append(dim)
        return 0

# Class 'ArregloNodo' creates objects that represent a specific item that the user is trying to access in the array 
class ArregloNodo():
    def __init__(self, name, elem, dim, baseMem, type, obj):
        self.obj = obj
        self.elem = self.parseElem(elem)
        self.type = type
        self.dim = dim
        self.name = name
        self.baseMem = baseMem
        self.validateObjDim()
        self.memadd  = self.calculateMemAddress()

    # Changes elem items into integers and adds them to a list
    def parseElem(self, p):
        r = []
        for i in p:
            r.append(int(i))
        return r

    # Calculates memory address based on the current base memory and element the user wants to access
    def calculateMemAddress(self):
        if self.dim == 1:
            return self.baseMem + self.elem[0]
        elif self.dim == 2:
            return self.baseMem + self.elem[0] * self.obj.arrNodes[1] + self.elem[1]

    # Validates element the user wants to access is within boundaries of array dimensions
    def validateObjDim(self):
        cont = 0
        if len(self.elem) != len(self.obj.arrNodes):
            raise Exception("Wrong array dimension")

        while(cont < self.dim):
            if self.obj.arrNodes[cont] <= self.elem[cont]:
                raise Exception("Out of bounds array")
            cont+=1
        return