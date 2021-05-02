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
        if(self.functions[scope]['values'][nombreVar]["tipo"] == "INT"):
            val = int(val)
        self.functions[scope]['values'][nombreVar]["valor"] = val

    def addVarNormalScope(self, var, scope, val):
        var = self.util.flatten(var)
        if(var[0].gettokentype() == "INT" and val != ""):
            val = int(val)
        self.functions[scope]["values"][var[1].value] = {"tipo" : var[0].gettokentype(), "valor" : val }
    
    def declareFuncInSymbolTable(self,p):
        self.functions[p[2].value] = {"tipo" : p[0].value, "values" : {}}

    def declareTempScope(self,cont, prevScope):
        self.functions["tempScope" + str(cont)] = {"values" : {}, "tipo": "null"}
        currDic = self.functions["tempScope" + str(cont)]
        prevDic = self.functions[prevScope]
        finalVals = copy.deepcopy(prevDic)
        self.util.mergeDictionaries(finalVals, currDic)
        return 0

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
        # self.currentScope.clear()
        self.currFuncNum+= 1
    
    # LOOKUP FUNCTIONS
    def lookupType(self,nombreVar, scope):
        currScopeVals = self.functions[scope]['values']
        if nombreVar in currScopeVals:
            return currScopeVals[nombreVar]["tipo"]
        else:
            raise Exception("!! EXC Variable", nombreVar, "not declared", "scope", scope, "!!")

    def lookupValue(self,nombreVar, scope):
        currScopeVals = self.functions[scope]['values']
        if nombreVar in currScopeVals:
            return currScopeVals[nombreVar]["valor"]
        else:
            raise Exception("!! EXC Variable", nombreVar, "not declared", "scope", scope, "!!")

    # PRINT FUNCTIONS
    def printSt(self):
        print("All table")
        pp.pprint(self.functions)

    def printCurrScope(self):
        print("Curr scope")
        pp.pprint(self.currentScope)

    # SYMBOL TABLE SPECIFIC HELPER FUNCS
            
    def assignVariableVal(self, var, scope):
        isComp = self.checkCompability(var[0].value, var[2].value, scope, 0)
        if(isComp):
            var[2] = isComp
            self.addValue(var[0].value, isComp, scope)
        else:
            print("Could not assign !", var)

    def clearScope(self, scope):
        del self.functions[scope]


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