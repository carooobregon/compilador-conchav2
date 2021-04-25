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
            self.currentScope[var[1].value] = {"tipo" : var[0].gettokentype(), "valor" : -9999 }
        else:
            self.currentScope[var[1].value] = {"tipo" : "arr_" + var[0].gettokentype(), "valor" : -9999, "size": var[2][1].value}

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
    
    def flatten(self,miLista):
        if miLista == []:
            return miLista
        if isinstance(miLista[0], list):
            return self.flatten(miLista[0]) + self.flatten(miLista[1:])
        return miLista[:1] + self.flatten(miLista[1:])

    def processParams(self, params):
        listaParams = []
        for i in params:
            if  isinstance(i, list):
                listaParams = self.flatten(i)
            listaParams.append(i)
        cont = 0
        while cont < len(listaParams)-1:
            self.currentScope[listaParams[cont+1].value] = {"tipo": listaParams[cont].gettokentype(),"valor": -99999}
            cont +=3

    def lookupType(self,nombreVar):
        # myType = self.currentScope[nombreVar]['tipo']
        if nombreVar in self.currentScope:
            print(self.currentScope[nombreVar]['tipo'])
            return self.currentScope[nombreVar]['tipo']
        else:
            print("Variable", nombreVar, " not declared")
            return "error"

    def printCurrScope(self):
        pp.pprint(self.currentScope)

    def addValue(self, nombreVar, val):
        self.currentScope[nombreVar]['valor'] = val
        print("ass(igned)", nombreVar, val)
        self.printCurrScope()