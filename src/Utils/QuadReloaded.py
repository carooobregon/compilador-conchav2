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
    pendientesJumps = Stack()

    def __init__(self):
        pass
    
    def pushQuadArithmeticQueue(self, q):
        for i in q.items:
            # print("INSERTING ", i)
            self.filaPrincipal.push(i)
        
        # self.printFilaPrincipal()

    # TODO: completar esto jsjsf
    def parsePrint(self,p):
        for i in p:
            if isinstance(i,str):
                self.filaPrincipal.push(["write", i])
            else:
                self.filaPrincipal.push(["write", i.value])
    
    def printFilaPrincipal(self):
        print("FILA PRINCIPAL")
        cont = 0 
        for i in self.filaPrincipal.items:
            print(cont+1,i)
            cont += 1
        print("FIN PRINCIPAL")
    
    def pushFilaPrincipal(self, a):
        self.filaPrincipal.push(a)

    def pushJumpPendiente(self):
        self.pendientesJumps.push(self.filaPrincipal.size()-1)

    def pushJumpPendienteSize(self):
        self.pendientesJumps.push(self.filaPrincipal.size())

    def pushJumpFirstWhile(self):
        self.pendientesJumps.push(self.filaPrincipal.size()+1)

    def updateJumpPendiente(self):
        self.filaPrincipal.items[self.pendientesJumps.peek()][1] = self.filaPrincipal.size()+1
        self.pendientesJumps.pop()

    def finWhile(self):
        end = self.pendientesJumps.pop()
        ret = self.pendientesJumps.pop()
        self.pushFilaPrincipal(["Goto", ret])
        self.filaPrincipal.items[end-1][1] = self.filaPrincipal.size()+1
    
    def currPrincipalCounter(self):
        return self.filaPrincipal.size()