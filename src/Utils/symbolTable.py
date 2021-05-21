from rply import ParserGenerator
import pprint
import copy
import queue
import math
from Utils.UtilFuncs import UtilFuncs
from Utils.semantic import SemanticCube
from Utils.Memoria import Memoria
pp = pprint.PrettyPrinter(indent=4)

class SymbolTable:
    util = UtilFuncs()
    def __init__(self):
        self.functions={"global" : {"values" : {}}}
        self.currentScope ={}
        self.currFuncNum = 0
        self.functionNameQ = queue.Queue()
        self.st = SemanticCube()

    # ADD FUNCTIONS

    def addVarNormalScope(self, varName, scope, varType):
        self.functions[scope]["values"][varName] = {"tipo" : varType}
    
    def declareFuncInSymbolTable(self,p):
        self.functions[p[1].value] = {"tipo" : p[0].value, "values" : {}, "parms": {}}

    def addTempVars(self, n, scope):
        self.functions[scope]["tempVars"] = n

    # PROCESSING FUNCTIONS    
    def processVars(self,vars, tipo, scope, memoria):
        plana = self.util.flatten(vars)
        cont = 0
        dir = 0
        for i in plana:
            if(i.value != ','):
                currDir = memoria.addVar(scope, tipo.gettokentype())
                self.functions[scope]["values"][i.value] = {"tipo" : tipo.gettokentype(), "dir" : currDir}
                cont += 1
        self.functions[scope]["localvars"] = cont

    def addQuadCounterFunc(self, counter, scope):
        self.functions[scope]["quadCounter"] = counter+1

    def procesSingleParam(self, params, listaParams, orderedParms, count):
        listaParams.append(params[0])
        listaParams.append(params[1])
        flatparms = self.util.flatten(params)     
        orderedParms.append(self.util.convertTypes(flatparms[0].value))
        count +=3
        return listaParams, orderedParms, count

    def processManyParams(self, params, listaParams, orderedParms, count):
        for i in params:
            if  isinstance(i, list):
                listaParams = self.util.flatten(i)
        listaParams.append(',')
        listaParams.append(params[0])
        listaParams.append(params[1])
        flatparms = self.util.flatten(params)     
        while(count < len(flatparms)):
            orderedParms.append(self.util.convertTypes(flatparms[count].value))
            count +=3 
        return listaParams, orderedParms, count

    def getListaParams(self, params, listaParams, orderedParms, count):
        if len(params) < 3:
            listaParams, orderedParms, count = self.procesSingleParam(params, listaParams, orderedParms, count)
        else:
            listaParams, orderedParms, count = self.processManyParams(params, listaParams, orderedParms, count)

    def processParams(self, params, scope):
        listaParams = []
        count = 0
        orderedParms = []
        self.functions[scope]["parms"] = []
        self.getListaParams(params, listaParams, orderedParms, count)
        if len(params) < 3:
            listaParams, orderedParms, count = self.procesSingleParam(params, listaParams, orderedParms, count)
        else:
            listaParams, orderedParms, count = self.processManyParams(params, listaParams, orderedParms, count)

        self.functions[scope]["parms"] = orderedParms
        return listaParams
    
    def getParams(self, scope):
        return self.functions[scope]["parms"]

    # retvalue, nombre, params
    def processFuncDeclP(self, p):
        listaParams = ""
        self.declareFuncInSymbolTable(p)
        if(len(p[3]) > 0):
            listaParams = self.processParams(p[3], p[1].value)
        cont = 0
        while cont < len(listaParams)-1:
            self.functions[p[1].value]["values"][listaParams[cont+1].value] = {"tipo": listaParams[cont].gettokentype()}
            # self.functions[p[1].value]["parms"].append(listaParams[cont].gettokentype())
            cont +=3
        # self.functions[p[1].value]["values"] = dict(self.functions[p[1].value]["values"].items() + self.functions["global"]["values"].items())

    def closeCurrScope(self, funcName, funcRet):
        finalVals = copy.deepcopy(self.currentScope)
        if funcName in self.functions:
            self.util.mergeDictionaries(self.functions[funcName], finalVals)
        self.functions[funcName] = {"values" : finalVals, "tipo" : funcRet}
        # self.currentScope.clear()
        self.currFuncNum+= 1
    
    # LOOKUP FUNCTIONS
    def lookupquadCounter(self, scope):
        return self.functions[scope]['quadCounter']

    def lookupType(self,nombreVar, scope):
        currScopeVals = self.functions[scope]['values']
        if nombreVar in currScopeVals:
            return currScopeVals[nombreVar]["tipo"]
        else:
            raise Exception("!! Type EXC Variable", nombreVar, "not declared", "scope", scope, "!!")
    
    def lookupVar(self,nombreVar, scope):
        currScopeVals = self.functions[scope]['values']
        if nombreVar in currScopeVals:
            return nombreVar
        else:
            raise Exception("!! Var EXC Variable", nombreVar, "not declared", "scope", scope, "!!")
    def lookupFunction(self, nombreFunc):
        allFuncNames = self.functions
        if nombreFunc in allFuncNames:
            return True
        else:
            raise Exception("!! Func", nombreFunc, "not declared !!")
            return False
    

    # PRINT FUNCTIONS
    def printSt(self):
        print("All table")
        pp.pprint(self.functions)

    def printCurrScope(self):
        print("Curr scope")
        pp.pprint(self.currentScope)

    # SYMBOL TABLE SPECIFIC HELPER FUNCS

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

        