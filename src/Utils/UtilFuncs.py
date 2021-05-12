from Utils.Stack import Stack
from queue import Queue

class UtilFuncs:
    funcStack = Stack()

    def __init__(self):
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
        if(tipo == 'entero') or isinstance(tipo, int):
            return "INT"
        if(tipo == 'flotante') or isinstance(tipo, float):
            return "FLOT"
        if(tipo == 'cadena') or isinstance(tipo, str):
            return "STR"
        if(tipo == 'booleano') or isinstance(tipo, bool):
            return "BOOL"
        print("returning token type")
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