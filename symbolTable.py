from os import replace
from rply import ParserGenerator
import pprint
import copy

pp = pprint.PrettyPrinter(indent=4)

class SymbolTable:
    def __init__(self):
        self.functions={}
        self.currentScope ={}
        self.currFuncNum = 0
    
    def addVarCurrScope(self, var):
        if(len(var) < 4):
            self.currentScope[var[1].value] = {"tipo" : var[0].value, "valor" : -9999 }
        else:
            self.currentScope[var[1].value] = {"tipo" : "arr_" + var[0].value, "valor" : -9999}
        print("currsco", self.currentScope)
    
    def closeCurrScope(self, f):
        self.functions[0] = {"values" : copy.deepcopy(self.currentScope), "tipo" : "null"}
        self.currentScope.clear()
        print("Func ", self.functions)
        print("Current ", self.currentScope)
        self.currFuncNum+= 1
    
    def printSymbolTable(self):
        pp.pprint(self.functions)

    def processFunction(self, p):
        self.replaceKey(p[2].value)
        self.addFunctionRetValue(p[2].value, p[0].value)

    def processMain(self):
        self.replaceKey("main")
        self.addFunctionRetValue("main", "vacio")

    def replaceKey(self, name):
        self.functions[name] = self.functions.pop(0)
    
    def addFunctionRetValue(self, name, ret):
        self.functions[name]["tipo"] = ret
        # self.functions[name].append(ret)