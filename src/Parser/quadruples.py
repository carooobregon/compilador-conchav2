# Quadruple generates the appropiate quadruple operations for arithmetic expressions

from Parser.Stack import Stack
from Parser.Queue import Queue
from Parser.semantic import SemanticCube
from Parser.UtilFuncs import UtilFuncs
from Parser.TempTable import TempObject
from Parser.Arreglo import ArregloNodo

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
    
    # EvaluateQuadruple is the main driver function to evaluate arithmetic expressions, it iterates through
    # an expression and follows left associativity for the operand heriarchy. If element is an opening parenthesis,
    # calls create parenthesisexpr that joins the inside expression of parenthesis and calls evaluate quadruple recursively.
    # When it encounters a number, temporal object or variable it gets its value and pushes it to the pilaOperandos stack 
    # and also pushes the type to pilaTipos
    # If it encounters an operation item such as sum, sub, it first checks if the top of the PEMDAs (named after Parentheses, Exponential, Mutliplication and Division)
    # has an element of its same heriarchy (another sum or sub), for it to perform a quad operation.
    # If the current top of pemdas stack is a multiplication or division, we get the element value and call mulOrDivOperation
    # After the loop goes through the expression, if there's a sum or sub operation waiting, we call sumorsuboperation
    # to generate quads
    # The answer is the top of the pilaOperandos, which is the operand stack, and the type on top of pilaTipos
    def evaluateQuadruple(self, expresion, table, scope, currTemp):
        self.currTempCounter = currTemp
        self.globalScope = scope
        cont = 0
        if(len(expresion) == 1):
            return self.currExpQuads, self.currTempCounter, self.tipo
        if(len(expresion) == 2):
            return self.getElementValue(expresion[0],table, scope, cont, expresion)
        pilaOperandos =  Stack()
        pilaTipos = Stack()
        pilaPEMDAS = Stack()
        cont = 0
        self.currExpresion = expresion
        while cont < len(expresion):
            i = expresion[cont]            
            if i == '(':
                parenBody = self.createParenthesisExpr(expresion[cont+1:])
                parenArr,currTemp,quadType = self.evaluateQuadruple(parenBody, table, scope, self.currTempCounter)
                cont += len(parenBody) + 1
                pilaOperandos.push(self.answer)
                pilaTipos.push(self.tipo)
                cont += self.skipForParens
                self.skipForParens = 0
            elif isinstance(i, float) or isinstance(i, int) or isinstance(i, TempObject) or isinstance(i, ArregloNodo) or i.gettokentype() == 'INT' or i.gettokentype() == 'FLOT' or i.gettokentype() == 'ID':
                currElemVal, currElemType = self.getElementValue(i,table, scope, cont,expresion)
                pilaOperandos.push(currElemVal)
                pilaTipos.push(currElemType)
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

    # Gets element value and returns a list that includes the expression and the value of current element, if
    # element is a parentheses, calls evaluatequadruple recursively to get value of expression inside
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

    # Generates quads necessary to perform ar sum or subtracting operation
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
        self.currExpQuads.push([topPemdasStack, leftOp, rightOp, tempN])

    # Generates quads necessary to perform ar multiplication or division operation
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

    # Generates quads necessary to perform a parenthesis expresion
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