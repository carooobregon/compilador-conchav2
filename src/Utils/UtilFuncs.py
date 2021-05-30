from Utils.Stack import Stack
from Utils.Queue import Queue
from Utils.TempTable import TempObject

# from Utils.quadruples import Quadruple
import copy

class UtilFuncs:
    funcStack = Stack()
    # qd = Quadruple()

    def __init__(self):
        self.currParams = []
        pass
        # self.functionNameQ = Queue()

    def addFunctionNameQ(self, f):
        self.funcStack.push(f)

    def getLatestFuncNameQ(self):
        if(self.funcStack.isEmpty()):
            return "na"
        else:
            func = self.funcStack.peek()
            self.funcStack.pop()
            return func
    
    def flatten(self,miLista):
        if miLista == []:
            return miLista
        if isinstance(miLista[0], list):
            return self.flatten(miLista[0]) + self.flatten(miLista[1:])
        return miLista[:1] + self.flatten(miLista[1:])

    def mergeDictionaries(self, dict1, dict2):
        return(dict2.update(dict1))
    
    def convertTypes(self, tipo):
        if(tipo == 'entero') or tipo == 'INT' or isinstance(tipo, int):
            return "INT"
        if(tipo == 'flotante') or tipo == 'FLOT' or isinstance(tipo, float):
            return "FLOT"
        ## todo checar si borrar esto
        if(tipo == 'ID'):
            return "ID"
        if(tipo == 'cadena') or tipo == 'STR' or isinstance(tipo, str):
            return "STR"
        if(tipo == 'booleano') or tipo == 'BOOL' or isinstance(tipo, bool):
            return "BOOL"
        return tipo.gettokentype()
    
    def getValue(self, val):
        if isinstance(val, int):
            return val
        elif isinstance(val,float):
            return val
        elif isinstance(val, str):
            return val
        elif isinstance(val, bool):
            return val
        elif isinstance(val, TempObject):
            return val
        return val.value

    def addParamList(self, val):
        self.currParams.insert(0,val)
    
    def printParamList(self):
        print("Param List")
        print(self.currParams)

    def getParamList(self):
        params = copy.deepcopy(self.currParams)
        self.currParams = []
        return params


    def getIdxForMemory(self, type):
        if type == 'INT':
            return 0
        elif type == 'FLOT':
            return 1
        elif type == 'BOOL':
            return 2
        elif type == 'STR':
            return 3
        
    def handlePrintStatements(self, lista, st, currentScope, currGlobal, quadreload, qd, temp, mem, const):
        for i in lista:
            i = self.flatten(i)
            fin = ""
            if(len(i) > 1):
                q, currTemp, quadType = qd.evaluateQuadruple(i, st, currentScope, currGlobal)
                nuevaQ = copy.deepcopy(q)
                qd.clearQueue()
                temp.transformTemps(nuevaQ.items,mem)
                currGlobal = currTemp
                quadreload.pushQuadArithmeticQueue(nuevaQ, temp, const, st, currentScope)
                fin = nuevaQ.tail()[3]
            else:
                fin = self.getValue(i[0])
            quadreload.parsePrint(fin, temp, const, st, currentScope)
        return currGlobal
    
    def handleReadStatement(self,lista, st, currentScope, currGlobal, quadreload, qd, temp, mem, const):
        print("estoy entrando aqui")
        