from Utils.Stack import Stack
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs



class Quadruple:

    ut = UtilFuncs()
    sCube = SemanticCube()

    pilaOperandos =  Stack()
    pilaTipos = Stack()
    pilaPEMDAS = Stack()

    def __init__(self):
        pass

    def evaluateQuadruple(self, expresion, table, scope):
        #print(" DEBUG QUADS ", expresion, len(expresion))
        for i in expresion:
            currElemType = self.getElementType(i,table, scope) 
            currElemVal = self.getElementValue(i,table, scope) 
            if currElemType == 'CTE_ENT' or currElemType == 'CTE_FLOT' or currElemType == 'INT' or currElemType == 'FLOT':
                self.pilaOperandos.push(currElemVal)
                self.pilaTipos.push(currElemType)
            elif currElemType == 'SUM' or currElemType == 'SUB' or currElemType == 'MUL' or currElemType == 'DIV':
                self.pilaPEMDAS.push(currElemType)

        print(" operandos ")
        self.pilaOperandos.print()
        print(" tipos ")
        self.pilaTipos.print()
        print(" pemdas ")
        self.pilaPEMDAS.print()


    def getElementType(self,expresion,table, scope):
        if expresion.gettokentype() == 'ID':
            tipoExp = table.lookupType(expresion.value, scope)
        else:
            tipoExp = expresion.gettokentype()
        
        return tipoExp

    def getElementValue(self,expresion,table, scope):
        if expresion.gettokentype() == 'ID':
            tipoExp = table.lookupValue(expresion.value, scope)
        else:
            tipoExp = expresion.value
        
        return tipoExp




