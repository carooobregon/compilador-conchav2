from Parser.Arreglo import ArregloNodo
from Parser.Stack import Stack
from Parser.Queue import Queue
from Parser.TempTable import TempObject

# from Parser.quadruples import Quadruple
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
        if isinstance(tipo, TempObject) or isinstance(tipo, ArregloNodo):
            return tipo.type
        return tipo.gettokentype()
    
    def getValue(self, val):
        t = type(val)
        if isinstance(val, int):
            return val
        elif isinstance(val,float):
            return val
        elif isinstance(val, str):
            return val
        elif isinstance(val, bool):
            return val
        elif isinstance(val, TempObject) or isinstance(val, ArregloNodo):
            return val
        else:
            t = (type(val))
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
                nuevaQ, currTemp, quadType = qd.evaluateQuadruple(i, st, currentScope, currGlobal)
                temp.transformTemps(nuevaQ.items,mem)
                currGlobal = currTemp
                quadreload.pushQuadArithmeticQueue(nuevaQ, temp, const, st, currentScope)
                fin = nuevaQ.tail()[3]
                qd.clearQueue()
            else:
                fin = self.getValue(i[0])
            quadreload.parsePrint(fin, temp, const, st, currentScope)
        return currGlobal

    def finishFunc(self, st, currGlobal, currentScope, mem, funcTable):
        st.addTempVars(currGlobal, currentScope)
        funcInfo = st.getFunctionInfo(currentScope)
        tempCounters = mem.getTemps()
        funcTable.addFunction(funcInfo, currentScope, tempCounters)
        mem.resetLocal()
        currGlobal = 0
        currTempN = 1
        return currGlobal, currTempN, funcTable, mem
    
    def handleReadStatement(self,lista, st, currentScope, currGlobal, quadreload, qd, temp, mem, const):
        print("estoy entrando aqui")
        