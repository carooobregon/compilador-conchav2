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
    def __init__(self, name, elem, dim, baseMem, type, obj, dirmemoria):
        self.leftInf = 0;
        self.obj = obj
        self.elem = self.parseElem(elem)
        self.type = type
        self.dim = dim
        self.name = name
        self.baseMem = baseMem
        self.memadd = baseMem + 90
        self.spaces = []
        self.dirmemoria = dirmemoria
    # Changes elem items into integers and adds them to a list
    def parseElem(self, p):#arr[1234]
        print("token boi",p)
        return p
    
    def calculoElda(self,dimArr):
        tamano =  int(dimArr) -  self.leftInf + 1

        print("calculanding",tamano)
    
