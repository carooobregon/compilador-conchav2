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
        print("antesdelwhle", expresion)
        while cont < len(expresion): # flotante elda = (1 + ((3 * 5) / 6)) - (3 * 6);  => 14.5
            i = expresion[cont]
            print(i)
            
            # if(isinstance(i, float) or isinstance(i, int) or i.gettokentype() == "ID"):
            #     currElemVal, currElemType = self.getElementValue(i,table, scope, cont)
            #     print(currElemType, currElemVal)
            # elif i.gettokentype() == "LPARENS":
            #     print("ISPARENTHESIS")
            if i == '(':
                print("isparen!!")
                print("slice", expresion[cont+1:])
                parenBody = self.createParenthesisExpr(expresion[cont+1:])
                print("pb", parenBody)
                exp, tip = self.evaluateQuadruple(parenBody, table, scope)
                print("ans", exp)
                cont += len(parenBody) + 1
                pilaOperandos.push(exp)
                pilaTipos.push(tip)
                cont += self.skipForParens
                print("opop2")
                pilaOperandos.print()
                print("tiptip2")
                pilaTipos.print()
                self.skipForParens = 0
            elif isinstance(i, float) or isinstance(i, int) or i.gettokentype() == 'INT' or i.gettokentype() == 'FLOT' or i.gettokentype() == 'ID':
                currElemVal, currElemType = self.getElementValue(i,table, scope, cont,expresion)
                print(currElemType, currElemVal)
                pilaOperandos.push(currElemVal) # 1
                pilaTipos.push(currElemType) # int
                print("aquii", currElemVal, currElemType)
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
        print("my ans", answer, "my tipo", tipo)
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
            print("exp", fullexp)
            parenBody = self.createParenthesisExpr(fullexp[cont+2:])
            print("parenb", parenBody)
            exp, tip = self.evaluateQuadruple(parenBody, table, scope)
            print("pbody", parenBody)
            self.skipForParens = len(parenBody) + 1
            tip = "INT"
            return [exp, tip]
        elif expresion.gettokentype() == 'ID':
            return [table.lookupValue(expresion.value, scope), table.lookupType(expresion.value, scope)]
        else:
            print("edgecasing", expresion)
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
        parenCounter = 1
        print("funfs", expresion)
        for i in expresion:
            if(i == '('):
                print("newparens")
                parenCounter +=1
                exp.append(i)
            elif not isinstance(i, int) and not isinstance(i, float) and i.value == ')':
                parenCounter -= 1
                print("close parens")
                if(parenCounter == 0):
                    print("parenexp", exp)
                    return exp
            else:
                if(i == '('):
                    parenCounter +=1
                exp.append(i)
        print("finfin", exp, parenCounter)
        return exp