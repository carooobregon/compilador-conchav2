from Utils.Stack import Stack
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs
from queue import Queue

class QuadReloaded:

    pilaTipos = Stack()
    pilaJumps = Stack()
    filaPrincipal = Queue()
    ut = UtilFuncs()

    def __init__(self):
        pass

    def getQuadArithmeticQueue(self, q):
        for i in q.queue:
            # print("INSERTING ", i)
            self.filaPrincipal.put(i)
        
        self.printFilaPrincipal()

    # TODO: completar esto jsjs
    def parsePrint(self,p):
        self.filaPrincipal.put(["write", p[2]])
        print(["write", p[2]])
        
    def printFilaPrincipal(self):
        print("FILA PRINCIPAL")
        for i in self.filaPrincipal.queue:
            print(i)