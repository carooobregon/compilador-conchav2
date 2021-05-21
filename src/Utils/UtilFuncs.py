from Utils.Stack import Stack
from Utils.Queue import Queue
import copy

class UtilFuncs:
    funcStack = Stack()

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
        else:
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

    def paramHandler(self, p):
        plana = self.ut.flatten(p[0])
        params = self.st.getParams(self.callingFunc)
        arg = ""
        accessParm = len(params) - self.currParm-1
        print("currparm", self.currParm, plana[0], plana)
        if(self.currParm+1 > len(params)):
            raise Exception("more params than expected", len(params))

        if(len(plana) == 1):
            soloparm = self.ut.convertTypes(plana[0])
            arg = self.ut.getValue(plana[0])
            # arg = plana[]
            if(soloparm == 'ID'):
                soloparm = self.st.lookupType(plana[0].value, self.currentScope)
            if(self.ut.convertTypes(soloparm) != params[accessParm]):
                raise Exception("!! different param type !! ", soloparm, " expected ", params[0])
        else:
            q, currTemp, quadType = self.qd.evaluateQuadruple(plana,self.st, self.currentScope,self.currGlobal)
            nuevaQ = copy.deepcopy(q)
            arg = "t" + str(currTemp)
            self.qd.clearQueue()
            self.currGlobal = currTemp
            self.reloadQuad.pushQuadArithmeticQueue(nuevaQ)
            print("mytype", quadType)
            print(accessParm)
            if(self.ut.convertTypes(quadType) != params[accessParm]):
                raise Exception("!! different param type !! ", quadType, " expected ", params[accessParm])
        # self.reloadQuad.pushFilaPrincipal(["PARAMETER", arg, "param" + str(self.currParm+1)])
        
        self.ut.addParamList(["PARAMETER", arg, "param" + str(accessParm+1)])
        self.currParm += 1

    def getIdxForMemory(self, type):
        if type == 'INT':
            return 0
        elif type == 'FLOT':
            return 1
        elif type == 'BOOL':
            return 2
        elif type == 'STR':
            return 3
