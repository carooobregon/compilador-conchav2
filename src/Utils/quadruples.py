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
        cont = 0
        if(len(expresion) == 2):
            return self.getElementValue(expresion[0],table, scope, cont,expresion)
        pilaOperandos =  Stack()
        pilaTipos = Stack()
        pilaPEMDAS = Stack()
        cont = 0
        self.currExpresion = expresion
        #Mult Div Add Sub            
        while cont < len(expresion): # flotante elda = (1 + ((3 * 5) / 6)) - (3 * 6);  => 14.5
            i = expresion[cont]            
            if i == '(':
                parenBody = self.createParenthesisExpr(expresion[cont+1:])
                exp, tip = self.evaluateQuadruple(parenBody, table, scope)
                cont += len(parenBody) + 1
                pilaOperandos.push(exp)
                pilaTipos.push(tip)
                cont += self.skipForParens
                self.skipForParens = 0
            elif isinstance(i, float) or isinstance(i, int) or i.gettokentype() == 'INT' or i.gettokentype() == 'FLOT' or i.gettokentype() == 'ID':
                currElemVal, currElemType = self.getElementValue(i,table, scope, cont,expresion)
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
                if(currPemdas == "MUL" or currPemdas == "DIV"):
                    rightOperand, rightType = self.getElementValue(expresion[cont+1],table,scope, cont, expresion)
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

    def getElementValue(self,expresion,table, scope, cont, fullexp):
        if isinstance(expresion,float):
            return [expresion, "FLOT"]
        elif isinstance(expresion,int):  
            return [expresion, "INT"]
        elif expresion == '(':
            parenBody = self.createParenthesisExpr(fullexp[cont+2:])
            exp, tip = self.evaluateQuadruple(parenBody, table, scope)
            self.skipForParens = len(parenBody) + 1
            tip = "INT"
            return [exp, tip]
        elif isinstance(expresion, str):
            return [expresion, "STRING"]
        elif isinstance(expresion, bool):
            return [expresion, "BOOL"]
        elif expresion.gettokentype() == 'ID':
            return [table.lookupValue(expresion.value, scope), table.lookupType(expresion.value, scope)]
        else:
            return [expresion, expresion.gettokentype()]

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

        resultType =  self.sCube.validateType(rightType,leftType)
                        
        if resultType != 'ERR':
            tempRes = self.getOperationResult(operator,leftOperand,rightOperand)
            pilaOperandos.push(tempRes )
            pilaTipos.push(resultType)
        else:
            print("ERROR: Type mismatch")

    def createParenthesisExpr(self, expresion):
        exp = []
        parenCounter = 1
        for i in expresion:
            if(i == '('):
                parenCounter +=1
                exp.append(i)
            elif not isinstance(i, int) and not isinstance(i, float) and i.value == ')':
                parenCounter -= 1
                if(parenCounter == 0):
                    return exp
                else:
                    exp.append(i)
            else:
                if(i == '('):
                    parenCounter +=1
                exp.append(i)
        return exp