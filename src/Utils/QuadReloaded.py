from Utils.Stack import Stack
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs
from Utils.Queue import Queue

class QuadReloaded:

    pilaTipos = Stack()
    pilaJumps = Stack()
    filaPrincipal = Queue()
    ut = UtilFuncs()

    def __init__(self):
        pass

    def pushQuadArithmeticQueue(self, q):
        for i in q.items:
            # print("INSERTING ", i)
            self.filaPrincipal.push(i)
        
        self.printFilaPrincipal()

    # TODO: completar esto jsjs
    def parsePrint(self,p):
        self.filaPrincipal.push(["write", p[2]])
        print(["write", p[2]])
        
    def printFilaPrincipal(self):
        print("FILA PRINCIPAL")
        for i in self.filaPrincipal.items:
            print(i)
        print("FIN PRINCIPAL")