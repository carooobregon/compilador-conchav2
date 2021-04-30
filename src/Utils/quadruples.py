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

    pilaQuad = Stack()
    shouldAdd = True
    def __init__(self):
        pass

    def evaluateQuadruple(self, expresion, table, scope):
        #print(" DEBUG QUADS ", expresion, len(expresion))
        cont = 0
        #Mult Div Add Sub            
        while cont < len(expresion): # flotante elda = (1 + ((3 * 5) / 6)) - (3 * 6);  => 14.5
            i = expresion[cont] 
            currElemType = self.getElementType(i,table, scope) 
            currElemVal = self.getElementValue(i,table, scope) 
            typeOfPemdas = ''

            if currElemType == 'CTE_ENT' or currElemType == 'CTE_FLOT' or currElemType == 'INT' or currElemType == 'FLOT':
                self.pilaOperandos.push(currElemVal) # 1
                self.pilaTipos.push(currElemType) # int
            
            elif i.gettokentype() == 'SUM' or i.gettokentype() == 'SUB' or i.gettokentype() == 'MUL' or i.gettokentype() == 'DIV':
                currPemdas = i.gettokentype()
                if not self.pilaPEMDAS.isEmpty():
                    topPemdasStack = self.pilaPEMDAS.peek()
                    print("debug pemdas", currPemdas, topPemdasStack)
                    if((currPemdas == "SUM" and topPemdasStack == "SUM") or (currPemdas == "SUM" and topPemdasStack == "SUB") or (currPemdas == "SUB" and topPemdasStack == "SUB") or (currPemdas == "SUB" and topPemdasStack == "SUM")):
                        self.sumOrSubOperation(topPemdasStack)
                        self.shouldAdd = True
                if(currPemdas == "MUL" or currPemdas == "DIV"):
                    rightOperand = self.getElementValue(expresion[cont+1],table,scope)
                    rightType = self.getElementType(expresion[cont+1],table,scope)
                    self.mulOrDivOperation(currPemdas, [rightOperand, rightType])
                    cont += 1
                if(currPemdas == "SUM" or currPemdas == "SUB"):
                    self.pilaPEMDAS.push(i.gettokentype())
                    self.shouldAdd = False
            print("operandos")
            self.pilaOperandos.print()
            print(" tipos")
            self.pilaTipos.print()
            print(" pemdas")
            self.pilaPEMDAS.print()
            print("---------------------------------------------------------------------------------------")
            cont += 1
            
        print("---------------------------------------------------------------------------------------")
        print(" final operandos")
        self.pilaOperandos.print()
        print(" tipos")
        self.pilaTipos.print()
        print(" pemdas")
        self.pilaPEMDAS.print()
        cont = 0
        if not self.pilaPEMDAS.isEmpty():
            print("popping bottles")
            self.sumOrSubOperation(self.pilaPEMDAS.peek())
        print("---------------------------------------------------------------------------------------")
        print(" final bueno operandos")
        self.pilaOperandos.print()
        print(" tipos")
        self.pilaTipos.print()
        print(" pemdas")
        self.pilaPEMDAS.print()

    def getElementType(self,expresion,table, scope):
        if isinstance(expresion,float):
            return 'FLOT'
        elif isinstance(expresion,int):      
            return 'INT'
        
        elif expresion.gettokentype() == 'ID':
            return table.lookupType(expresion.value, scope)

    def getElementValue(self,expresion,table, scope):
        if isinstance(expresion,float) or isinstance(expresion,int):      
            return expresion

        elif expresion.gettokentype() == 'ID':
            return table.lookupValue(expresion.value, scope)


    def getOperationResult(self,operation,left,right):
        if operation == 'SUM':
            print(left," + ", right)
            return left + right

        elif operation == 'SUB':
            print(left," - ", right)
            return left - right

        elif operation == 'MUL':
            print(left," * ", right)
            return left * right
        
        else:
            print(left," / ", right)
            return left / right

    def sumOrSubOperation(self, topPemdasStack):
        print("doing operation")
        rightOp = self.pilaOperandos.pop()
        leftOp = self.pilaOperandos.pop()
        rightType = self.pilaTipos.pop()
        leftType = self.pilaTipos.pop()
        self.pilaPEMDAS.pop()
        operationRes = self.getOperationResult(topPemdasStack, leftOp, rightOp)
        operationType = self.sCube.validateType(rightType,leftType)
        self.pilaOperandos.push(operationRes)
        self.pilaTipos.push(operationType)
    
    def mulOrDivOperation(self, currPemdas, rightOp):
        print("doing mul operation")
        rightOperand = rightOp[0]
        rightType = rightOp[1]

        leftOperand = self.pilaOperandos.pop()
        leftType = self.pilaTipos.pop()
                        
        operator = currPemdas

        resultType =  self.sCube.validateType(rightType,leftType)
                        
        if resultType != 'ERR':
            tempRes = self.getOperationResult(operator,leftOperand,rightOperand)
            tempCuad = [operator, leftOperand, rightOperand, tempRes ]
            self.pilaQuad.push(tempCuad)

            self.pilaOperandos.push(tempRes )
            self.pilaTipos.push(resultType)
        else:
            print("ERROR: Type mismatch")