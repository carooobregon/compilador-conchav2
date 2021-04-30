from os import replace
from rply import ParserGenerator
import pprint
import copy
import queue
import math
from Utils.UtilFuncs import UtilFuncs
from Utils.semantic import SemanticCube

pp = pprint.PrettyPrinter(indent=4)

class SymbolTable:
    util = UtilFuncs()
    def __init__(self):
        self.functions={"main" : {"tipo" : "vacio", "values" : {}}}
        self.currentScope ={}
        self.currFuncNum = 0
        self.functionNameQ = queue.Queue()
        self.st = SemanticCube()

    # ADD FUNCTIONS
    def addValue(self, nombreVar, val, scope):
        self.functions[scope]['values'][nombreVar]["valor"] = val

    def addVarNormalScope(self, var, scope, val):
        var = self.util.flatten(var)
        self.functions[scope]["values"][var[1].value] = {"tipo" : var[0].gettokentype(), "valor" : val }
    
    def declareFuncInSymbolTable(self,p):
        self.functions[p[2].value] = {"tipo" : p[0].value, "values" : {}}

    # PROCESSING FUNCTIONS
    
    def processParams(self, params):
        listaParams = []
        if len(params) < 3:
            listaParams.append(params[0])
            listaParams.append(params[1])
        else:
            for i in params:
                if  isinstance(i, list):
                    listaParams = self.util.flatten(i)
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
            self.util.mergeDictionaries(self.functions[funcName]['values'], finalVals)
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
    def print(self):
        print("All table")
        pp.pprint(self.functions)

    def printCurrScope(self):
        print("Curr scope")
        pp.pprint(self.currentScope)

    # SYMBOL TABLE SPECIFIC HELPER FUNCS
            
    def declareVariableVal(self, var, scope):
        isComp = self.checkCompability(var[0].value, var[3].value, scope, 1)
        if(isComp):
            var[3] = isComp
            self.addVarNormalScope(var, scope, var[3])
        else:
            print("Could not assign !", var)

    def assignVariableVal(self, var, scope):
        isComp = self.checkCompability(var[0].value, var[2].value, scope, 0)
        if(isComp):
            var[2] = isComp
            self.addValue(var[0].value, isComp, scope)
        else:
            print("Could not assign !", var)

    def declareVariableInit(self, var, scope):
        #if(self.st.validateType(self.util.convertTypes(var[0].value), var[3].gettokentype())):
        if(self.st.validateType(self.util.convertTypes(var[0].value), var[3].gettokentype()) != 'ERR'):
            self.addVarNormalScope(var, scope, var[3].value)
            #print("val", var)
        else:
            print("noval", var)

    # UTIL FUNCS
    
    def checkCompability(self, varA, varB, scope, opType):
        if(opType == 1):
            tipoA = self.util.convertTypes(varA)
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