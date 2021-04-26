from os import replace
from rply import ParserGenerator
import pprint
import copy
import queue


pp = pprint.PrettyPrinter(indent=4)

class SymbolTable:
    def __init__(self):
        self.functions={}
        self.currentScope ={}
        self.currFuncNum = 0
        self.functionNameQ = queue.Queue()

    def Merge(self, dict1, dict2):
        print("dic1 ", dict1)
        print("dic2 ", dict2)
        return(dict2.update(dict1))

    def addVarCurrScope(self, var):
        if(len(var) < 4):
            self.currentScope[var[1].value] = {"tipo" : var[0].gettokentype(), "valor" : "" }
        else:
            self.currentScope[var[1].value] = {"tipo" : "arr_" + var[0].gettokentype(), "valor" : "", "size": var[2][1].value}

    def closeCurrScope(self, f, funcName, funcRet):
        finalVals = copy.deepcopy(self.currentScope)
        if funcName in self.functions:
            print("Has values", self.functions[funcName]['values'])
            self.Merge(self.functions[funcName]['values'], finalVals)
            print("newdick", finalVals)
        self.functions[funcName] = {"values" : finalVals, "tipo" : funcRet}
        self.currentScope.clear()
        self.currFuncNum+= 1
    
    def printSymbolTable(self):
        print("All table")
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
        listaParams.append(',')
        listaParams.append(params[0])
        listaParams.append(params[1])
        print("paa", listaParams)
        # coolParams = []
        # while cont < len(p[4])-1:
        #     self.functions[p[2].value]['values'] = {"tipo": listaParams[cont].gettokentype(),"valor": ""}
        #     cont +=3
        cont = 0
        return listaParams

    def processFuncDeclP(self, p):
        listaParams = self.processParams(p[4])
        print(p[4])
        print("adding", p[2].value, listaParams, p[0])
        self.functions[p[2].value] = {"tipo" : p[0].value, "values" : {}}
        cont = 0
        while cont < len(listaParams)-1:
            self.functions[p[2].value]['values'][listaParams[cont+1].value] = {"tipo": listaParams[cont].gettokentype(), "valor": ""}
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
        print("Curr scope")
        pp.pprint(self.currentScope)

    def addValue(self, nombreVar, val):
        self.currentScope[nombreVar]['valor'] = val
        print("ass(igned)", nombreVar, val)
        self.printCurrScope()
    
    def queueFuncNames(self, funcName):
        self.functionNameQ.get(funcName)