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
            self.currentScope[var[1].value] = {"tipo" : "arr_" + var[0].value, "valor" : -9999, "size": var[2][1].value}
            print("pretty")
            pp.pprint(var)
        print("currsco", self.currentScope)
    
    def closeCurrScope(self, f, funcName, funcRet):
        self.functions[funcName] = {"values" : copy.deepcopy(self.currentScope), "tipo" : funcRet}
        self.currentScope.clear()
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

    def processParams(self, p):
        print(type(p))
        pp.pprint(p)
        # flat_list = [item for sublist in p.value for item in sublist]
        # print("listt", flat_list)