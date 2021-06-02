# from Utils.symbolTable import SymbolTable
from Utils.Stack import Stack
from Utils.Queue import Queue
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs
from Utils.TempTable import TempObject
from Utils.Arreglo import ArregloNodo

class Quadruple:

    ut = UtilFuncs()
    sCube = SemanticCube()

    currExpresion = ""
    shouldAdd = True
    skipForParens = 0
    currExpQuads = Queue()
    answer = 0;
    tipo = "NONE"
    currTempCounter = 0
    globalScope = ""

    def __init__(self):
        pass

    def evaluateQuadruple(self, expresion, table, scope, currTemp):
        self.currTempCounter = currTemp
        self.globalScope = scope
        cont = 0
        ## self.currExpQuads, self.currTempCounter, self.tipo
        if(len(expresion) == 1):
            return self.currExpQuads, self.currTempCounter, self.tipo
        if(len(expresion) == 2):
            return self.getElementValue(expresion[0],table, scope, cont, expresion)
        pilaOperandos =  Stack()
        pilaTipos = Stack()
        pilaPEMDAS = Stack()
        cont = 0
        self.currExpresion = expresion
        #Mult Div Add Sub           
        # 3 + 3 -4 > 3 + ab 
        while cont < len(expresion): # flotante elda = (1 + ((3 * 5) / 6)) - (3 * 6);  => 14.5
            i = expresion[cont]            
            if i == '(':
                parenBody = self.createParenthesisExpr(expresion[cont+1:])
                parenArr,currTemp,quadType = self.evaluateQuadruple(parenBody, table, scope, self.currTempCounter)
                # parenQ, answerParenQ, currTemp, tipoParenQ = self.evaluateQuadruple(parenBody, table, scope,currTemp)
                cont += len(parenBody) + 1
                pilaOperandos.push(self.answer)
                pilaTipos.push(self.tipo)
                cont += self.skipForParens
                self.skipForParens = 0
            elif isinstance(i, float) or isinstance(i, int) or isinstance(i, TempObject) or isinstance(i, ArregloNodo) or i.gettokentype() == 'INT' or i.gettokentype() == 'FLOT' or i.gettokentype() == 'ID':
                currElemVal, currElemType = self.getElementValue(i,table, scope, cont,expresion)
                pilaOperandos.push(currElemVal) # 1
                pilaTipos.push(currElemType) # int
            elif i.gettokentype() == 'SUM' or i.gettokentype() == 'SUB' or i.gettokentype() == 'MUL' or i.gettokentype() == 'DIV':
                currPemdas = i.gettokentype()
                if not pilaPEMDAS.isEmpty():
                    topPemdasStack = pilaPEMDAS.peek()
                    if((currPemdas == "SUM" and topPemdasStack == "SUM") or (currPemdas == "SUM" and topPemdasStack == "SUB") or (currPemdas == "SUB" and topPemdasStack == "SUB") or (currPemdas == "SUB" and topPemdasStack == "SUM")):
                        self.sumOrSubOperation(topPemdasStack, pilaOperandos, pilaTipos, table)
                        pilaPEMDAS.pop()
                        self.shouldAdd = True
                if(currPemdas == "MUL" or currPemdas == "DIV"):
                    rightOperand, rightType = self.getElementValue(expresion[cont+1],table,scope, cont, expresion)
                    self.mulOrDivOperation(currPemdas, [rightOperand, rightType], pilaOperandos, pilaTipos, currPemdas, table)
                    cont += 1
                    cont += self.skipForParens
                    self.skipForParens = 0
                if(currPemdas == "SUM" or currPemdas == "SUB"):
                    pilaPEMDAS.push(i.gettokentype())
                    self.shouldAdd = False

            cont += 1
            
        cont = 0
        if not pilaPEMDAS.isEmpty():
            self.sumOrSubOperation(pilaPEMDAS.peek(), pilaOperandos, pilaTipos, table)
        self.answer = pilaOperandos.peek()
        self.tipo = pilaTipos.peek()
        pilaOperandos.clear()
        pilaTipos.clear()
        pilaPEMDAS.clear()
        return self.currExpQuads, self.currTempCounter, self.tipo

    def getElementValue(self,expresion,table, scope, cont, fullexp):
        if isinstance(expresion, TempObject) or isinstance(expresion, ArregloNodo):
            return [expresion, expresion.type]
        if isinstance(expresion,float):
            return [expresion, "FLOT"]
        elif isinstance(expresion,int):  
            return [expresion, "INT"]
        elif expresion == '(':
            parenBody = self.createParenthesisExpr(fullexp[cont+2:])
            exp,currTemp, quadType = self.evaluateQuadruple(parenBody, table, scope, self.currTempCounter)
            self.skipForParens = len(parenBody) + 1
            tip = "INT"
            return [self.answer, self.tipo]
        elif isinstance(expresion, str):
            return [expresion, "STRING"]
        elif isinstance(expresion, bool):
            return [expresion, "BOOL"]
        elif expresion.gettokentype() == 'ID':
            return [table.lookupVar(expresion.value, scope), table.lookupType(expresion.value, scope)]
        else:
            return [expresion, expresion.gettokentype()]

    def getOperationResult(self,operation,left,right):
        if operation == 'SUM':
            return left + right

        elif operation == 'SUB':
            return left - right

        elif operation == 'MUL':
            return left * right

        elif operation == 'DIV':
            return left / right
            
        elif operation == 'MOTHN':
            return left > right

        elif operation == 'LETHN':
            return left < right

        elif operation == 'NEQ':
            return left != right
        
        elif operation == 'EQUALITY':
            return left == right
        else:
            raise Exception("Weird operation check syntax")
    
    def sumOrSubOperation(self, topPemdasStack, pilaOperandos, pilaTipos, st):
        self.currTempCounter += 1
        rightType = pilaTipos.pop()
        leftType = pilaTipos.pop()
        rightOp = pilaOperandos.pop()
        leftOp = pilaOperandos.pop()
        operationType = self.sCube.validateType(rightType,leftType)
        tempN = TempObject(operationType, self.currTempCounter)
        pilaOperandos.push(tempN)
        pilaTipos.push(operationType)
        # print("TIPOS sum or sub", type(leftOp), type(rightOp))
        self.currExpQuads.push([topPemdasStack, leftOp, rightOp, tempN])
    
    def mulOrDivOperation(self, currPemdas, rightOp, pilaOperandos, pilaTipos, topPemdasStack, st):
        rightOperand = rightOp[0]
        rightType = rightOp[1]

        leftOperand = pilaOperandos.pop()
        leftType = pilaTipos.pop()

        operator = currPemdas
        
        resultType =  self.sCube.validateType(rightType,leftType)
        if resultType != 'ERR':
            self.currTempCounter += 1
            tempN = TempObject(resultType, self.currTempCounter)
            self.currExpQuads.push([topPemdasStack, leftOperand, rightOperand, tempN])
            pilaOperandos.push(tempN)
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

    def clearQueue(self):
        self.currExpQuads.clear()