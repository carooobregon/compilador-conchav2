from Utils.Stack import Stack
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube



class Quadruple:

    pilaOperandos =  Stack()
    pilaTipos = Stack()
    pilaPEMDAS = Stack()

    def __init__(self):
        pass

    def evaluateQuadruple(self, expresion):
        print(" DEBUG QUADS ", expresion)

