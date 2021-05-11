from Utils.Stack import Stack
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs

class QuadReloaded:

    pilaTipos = Stack()
    pilaJumps = Stack()
    pilaPrincipal = Stack()
    ut = UtilFuncs()

    def __init__(self):
        pass


    # TODO: completar esto jsjs
    def parsePrint(self,p):
        self.pilaPrincipal.push(["write", p[2]])
        print(["write", p[2]])
        