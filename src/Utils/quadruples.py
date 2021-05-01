from Utils.Stack import Stack
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs

class Quadruple:

    ut = UtilFuncs()
    sCube = SemanticCube()

    currExpresion = ""
    shouldAdd = True
    skipForParens = 0

    def __init__(self):
        pass

    def evaluateQuadruple(self, expresion, table, scope):
        #print(" DEBUG QUADS ", expresion, len(expresion))
        pilaOperandos =  Stack()
        pilaTipos = Stack()
        pilaPEMDAS = Stack()
        cont = 0
        self.currExpresion = expresion
        #Mult Div Add Sub            
        while cont < len(expresion): # flotante elda = (1 + ((3 * 5) / 6)) - (3 * 6);  => 14.5
            i = expresion[cont]
            currElemVal, currElemType = self.getElementValue(i,table, scope, cont)
            if currElemType == 'CTE_ENT' or currElemType == 'CTE_FLOT' or currElemType == 'INT' or currElemType == 'FLOT':
                pilaOperandos.push(currElemVal) # 1
                pilaTipos.push(currElemType) # int
            elif i.gettokentype() == 'SUM' or i.gettokentype() == 'SUB' or i.gettokentype() == 'MUL' or i.gettokentype() == 'DIV':
                currPemdas = i.gettokentype()
                if not pilaPEMDAS.isEmpty():
                    topPemdasStack = pilaPEMDAS.peek()
                    if((currPemdas == "SUM" and topPemdasStack == "SUM") or (currPemdas == "SUM" and topPemdasStack == "SUB") or (currPemdas == "SUB" and topPemdasStack == "SUB") or (currPemdas == "SUB" and topPemdasStack == "SUM")):
                        self.sumOrSubOperation(topPemdasStack, pilaOperandos, pilaTipos)
                        pilaPEMDAS.pop()
                        self.shouldAdd = True
                if(currPemdas == "MUL" or currPemdas == "DIV") and not currPemdas == "LPARENS" or currPemdas == "RPARENS":
                    rightOperand, rightType = self.getElementValue(expresion[cont+1],table,scope, cont)
                    print(rightOperand)
                    self.mulOrDivOperation(currPemdas, [rightOperand, rightType], pilaOperandos, pilaTipos)
                    cont += 1
                    cont += self.skipForParens
                    self.skipForParens = 0
                if(currPemdas == "SUM" or currPemdas == "SUB"):
                    pilaPEMDAS.push(i.gettokentype())
                    self.shouldAdd = False
            cont += 1
            
        cont = 0
        if not pilaPEMDAS.isEmpty():
            self.sumOrSubOperation(pilaPEMDAS.peek(), pilaOperandos, pilaTipos)
        answer = pilaOperandos.peek()
        tipo = pilaTipos.peek()
        pilaOperandos.clear()
        pilaTipos.clear()
        pilaPEMDAS.clear()
        return answer, tipo

    def getElementType(self,expresion,table, scope):
        if isinstance(expresion,float):
            return 'FLOT'
        elif isinstance(expresion,int):      
            return 'INT'
        elif expresion.gettokentype() == 'ID':
            return table.lookupType(expresion.value, scope)
        elif expresion.gettokentype() == 'LPARENS':
            print("entrando al otro wey")
            return "INT"

    def getElementValue(self,expresion,table, scope, cont):
        if isinstance(expresion,float):
            return [expresion, "FLOT"]
        elif isinstance(expresion,int):  
            return [expresion, "INT"]
        elif expresion.gettokentype() == 'ID':
            return [table.lookupValue(expresion.value, scope), table.lookupType(expresion.value, scope)]
        elif expresion.gettokentype() == 'LPARENS':
            parenBody = self.createParenthesisExpr(self.currExpresion[cont+2:])
            exp, tip = self.evaluateQuadruple(parenBody, table, scope)
            self.skipForParens = len(parenBody) + 1
            tip = "INT"
            return [exp, tip]
        else:
            return [expresion, "operador"]

    def getOperationResult(self,operation,left,right):
        if operation == 'SUM':
            return left + right

        elif operation == 'SUB':
            return left - right

        elif operation == 'MUL':
            return left * right
        else:
            return left / right

    def sumOrSubOperation(self, topPemdasStack, pilaOperandos, pilaTipos):
        rightOp = pilaOperandos.pop()
        leftOp = pilaOperandos.pop()
        rightType = pilaTipos.pop()
        leftType = pilaTipos.pop()
        operationRes = self.getOperationResult(topPemdasStack, leftOp, rightOp)
        operationType = self.sCube.validateType(rightType,leftType)
        pilaOperandos.push(operationRes)
        pilaTipos.push(operationType)
    
    def mulOrDivOperation(self, currPemdas, rightOp, pilaOperandos, pilaTipos):
        rightOperand = rightOp[0]
        rightType = rightOp[1]

        leftOperand = pilaOperandos.pop()
        leftType = pilaTipos.pop()

        operator = currPemdas
        print(rightOperand, leftOperand, operator)

        resultType =  self.sCube.validateType(rightType,leftType)
                        
        if resultType != 'ERR':
            tempRes = self.getOperationResult(operator,leftOperand,rightOperand)
            pilaOperandos.push(tempRes )
            pilaTipos.push(resultType)
        else:
            print("ERROR: Type mismatch")

    def createParenthesisExpr(self, expresion):
        exp = []
        for i in expresion:
            if not isinstance(i, int) and not isinstance(i, float) and i.value == ')':
                return exp
            else:
                exp.append(i)