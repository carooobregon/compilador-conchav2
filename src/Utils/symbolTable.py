from os import replace
from rply import ParserGenerator
import pprint
import copy
import queue
import math

pp = pprint.PrettyPrinter(indent=4)

class SymbolTable:
    def __init__(self):
        self.functions={"main" : {"tipo" : "vacio", "values" : {}}}
        self.currentScope ={}
        self.currFuncNum = 0
        self.functionNameQ = queue.Queue()

    # ADD FUNCTIONS
    def addValue(self, nombreVar, val, scope):
        self.functions[scope]['values'][nombreVar]["valor"] = val

    def addVarNormalScope(self, var, scope):
        self.functions[scope]["values"][var[1].value] = {"tipo" : var[0].gettokentype(), "valor" : "" }
    
    def addVarNormalScope_complex(self, var, scope):
        var = self.flatten(var)
        self.functions[scope]["values"][var[1].value] = {"tipo" : var[0].gettokentype(), "valor" : "NORMAL COMPLEX" }

    def addFunctionRetValue(self, name, ret):
        self.functions[name]["tipo"] = ret

    def declareFuncInSymbolTable(self,p):
        self.functions[p[2].value] = {"tipo" : p[0].value, "values" : {}}

    # PROCESSING FUNCTIONS
    def processFunction(self, p):
        self.replaceKey(p[2].value)
        self.addFunctionRetValue(p[2].value, p[0].value)
    
    def processParams(self, params):
        listaParams = []
        if len(params) < 3:
            listaParams.append(params[0])
            listaParams.append(params[1])
        else:
            for i in params:
                if  isinstance(i, list):
                    listaParams = self.flatten(i)
            listaParams.append(',')
            listaParams.append(params[0])
            listaParams.append(params[1])
        return listaParams

    def processFuncDeclP(self, p):
        listaParams = self.processParams(p[4])
        self.declareFuncInSymbolTable(p)
        cont = 0
        
        while cont < len(listaParams)-1:
            self.functions[p[2].value]['values'][listaParams[cont+1].value] = {"tipo": listaParams[cont].gettokentype(), "valor": ""}
            cont +=3

    def closeCurrScope(self, funcName, funcRet):
        finalVals = copy.deepcopy(self.currentScope)
        if funcName in self.functions:
            self.Merge(self.functions[funcName]['values'], finalVals)
        self.functions[funcName] = {"values" : finalVals, "tipo" : funcRet}
        self.currentScope.clear()
        self.currFuncNum+= 1
    
    # LOOKUP FUNCTIONS
    def lookupType(self,nombreVar, scope):
        currScopeVals = self.functions[scope]['values']
        if nombreVar in currScopeVals:
            return currScopeVals[nombreVar]["tipo"]
        else:
            print("Variable", nombreVar, "not declared", "scope", scope)
            return "error"

    def lookupValue(self,nombreVar, scope):
        currScopeVals = self.functions[scope]['values']
        if nombreVar in currScopeVals:
            return currScopeVals[nombreVar]["valor"]
        else:
            print("Variable", nombreVar, "not declared", "scope", scope)
            return "error"

    # PRINT FUNCTIONS
    def printSymbolTable(self):
        print("All table")
        pp.pprint(self.functions)

    def printCurrScope(self):
        print("Curr scope")
        pp.pprint(self.currentScope)

    # ST-SPECIFIC HELPER FUNCS
    def queueFuncNames(self, funcName):
        self.functionNameQ.get(funcName)

    def replaceKey(self, name):
        self.functions[name] = self.functions.pop(0)
            
    def declareVariableVal(self, var, scope):
        isComp = self.checkCompability(var[0].value, var[3].value, scope, 1)
        if(isComp):
            var[3] = isComp
            self.addVarNormalScope(var, scope)
        else:
            print("Could not assign !", var)

    def assignVariableVal(self, var, scope):
        isComp = self.checkCompability(var[0].value, var[2].value, scope, 0)
        if(isComp):
            var[2] = isComp
            self.addValue(var[0].value, isComp, scope)
        else:
            print("Could not assign !", var)

    # UTIL FUNCS
    def Merge(self, dict1, dict2):
        return(dict2.update(dict1))

    def flatten(self,miLista):
        if miLista == []:
            return miLista
        if isinstance(miLista[0], list):
            return self.flatten(miLista[0]) + self.flatten(miLista[1:])
        return miLista[:1] + self.flatten(miLista[1:])

    def convertTypes(self, tipo):
        if(tipo == 'entero'):
            return "INT"
        if(tipo == 'flotante'):
            return "FLOT"
        if(tipo == 'cadena'):
            return "STR"
        if(tipo == 'booleano'):
            return "BOOL"
    
    def checkCompability(self, varA, varB, scope, opType):
        if(opType == 1):
            tipoA = self.convertTypes(varA)
        else:
            tipoA = self.lookupType(varA, scope)
        tipoB = self.lookupType(varB, scope)
        # type 1 is declaration and type 0 is assignation            
        valueB = self.lookupValue(varB, scope)
        if(tipoA == "INT" and tipoB == "FLOT"):
            return math.trunc(valueB)
        if(tipoA == "BOOL" and (valueB == "verdadero" or valueB == "falso")):
            return valueB
        if(tipoA == "FLOT" and tipoB == "INT") or tipoA == tipoB:
            return valueB
        else:
            print("Not compatible", varA, tipoA, varB, tipoB)