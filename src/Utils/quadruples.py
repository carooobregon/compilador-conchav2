from Utils.Stack import Stack
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs



class Quadruple:

    st = SymbolTable()
    ut = UtilFuncs()
    sCube = SemanticCube()

    pilaOperandos =  Stack()
    pilaTipos = Stack()
    pilaPEMDAS = Stack()

    def __init__(self):
        pass

    def evaluateQuadruple(self, expresion):
        plana = self.st.flatten(expresion)
        print(" DEBUG QUADS ", plana, len(plana))

