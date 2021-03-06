from rply import ParserGenerator
import pprint
import copy
import queue
import math
from Parser.UtilFuncs import UtilFuncs
from Parser.semantic import SemanticCube
from Parser.Memoria import Memoria
from Parser.ParamHandler import ParamHandler
from Parser.Arreglo import Arreglo
pp = pprint.PrettyPrinter(indent=4)

class SymbolTable:

    util = UtilFuncs()
    def __init__(self):
        self.functions={"global" : {"tempVars": -999, "quadCounter" : 0, "tipo": "np", "values" : {}, "varCounter": [0,0,0,0]}}
        self.currentScope ={}
        self.currFuncNum = 0
        self.functionNameQ = queue.Queue()
        self.st = SemanticCube()
        self.paramHandler = ParamHandler(self)
        self.ut = UtilFuncs()

    # ADD FUNCTIONS

    def addVarNormalScope(self, varName, scope, varType):
        self.functions[scope]["values"][varName] = {"tipo" : varType}
    
    def declareFuncInSymbolTable(self,p, memoria):
        if p[0].value != "vacio":
            tipoFunc = self.ut.convertTypes(p[0].value)
            currDir = memoria.addVar("global", tipoFunc)
            self.functions["global"]["values"][p[1].value] = {"tipo": tipoFunc, "dir": currDir}
            self.functions["global"]["varCounter"][memoria.getIdxForMemory(tipoFunc)] += 1
        else:
            tipoFunc = "vacio"
        self.functions[p[1].value] = {"tipo" : tipoFunc, "values" : {}, "parms": {}, "varCounter" : [0,0,0,0]}

    def addTempVars(self, n, scope):
        self.functions[scope]["tempVars"] = n
        
    def getFunctionInfo(self, scope):
        return self.functions[scope]

    def processObjVars(self,vars,tipo,scope,memoria):
        currDir = memoria.addVar(scope, tipo)
        self.functions[scope]["values"][vars] = {"tipo" : tipo, "dir" : currDir}
        self.functions[scope]["varCounter"][memoria.getIdxForMemory(tipo)] += 1
        self.functions[scope]["localvars"] += 1

    # PROCESSING FUNCTIONS    
    def processVars(self,vars, tipo, scope, memoria):
        plana = self.util.flatten(vars)
        cont = 0
        tipo = tipo.gettokentype()
        dir = 0
        toAdd = 0
        for i in plana:
            if isinstance(i, Arreglo) or i.value != ',':
                name = ""
                if isinstance(i, Arreglo):
                    currDir = memoria.addArray(i, tipo, scope)
                    name = i.name
                    toAdd = i.size
                    self.functions[scope]["values"][name] = {"tipo" : tipo, "dir" : currDir, "arrObj" : i}
                else:
                    currDir = memoria.addVar(scope, tipo)
                    name = i.value
                    toAdd = 1
                    self.functions[scope]["values"][name] = {"tipo" : tipo, "dir" : currDir}
                cont += 1
                self.functions[scope]["varCounter"][memoria.getIdxForMemory(tipo)] += toAdd
        self.functions[scope]["localvars"] = cont
        if "parms" in self.functions[scope]:
            self.functions[scope]["localvars"] += len(self.functions[scope]["parms"])

    def addArrayVar(self, var, tipo, scope, memoria):
        plana = self.util.flatten(vars)

    def addQuadCounterFunc(self, counter, scope):
        self.functions[scope]["quadCounter"] = counter+1
        
    def getParams(self, scope):
        return self.functions[scope]["parms"]

    # retvalue, nombre, params
    def processFuncDeclP(self, p, memoria):
        self.declareFuncInSymbolTable(p, memoria)
        self.paramHandler.updateParamObj(p[3], p[1].value, self, memoria)
        # paramHandler.addParamsLista()

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
        elif nombreVar in self.functions['global']['values']:
            return self.functions['global']['values'][nombreVar]["tipo"]
        else:
            raise Exception("!! Type EXC Variable", nombreVar, "not declared", "scope", scope, "!!")
    
    def lookupVar(self,nombreVar, scope):
        currScopeVals = self.functions[scope]['values']
        if nombreVar in currScopeVals or nombreVar in self.functions['global']['values']:
            return nombreVar
        else:
            raise Exception("!! Var EXC Variable", nombreVar, "not declared", "scope", scope, "!!")
    
    def lookupFunction(self, nombreFunc):
        allFuncNames = self.functions
        if nombreFunc in allFuncNames:
            return True
        else:
            raise Exception("!! Func", nombreFunc, "not declared !!")

    def lookupVariableAddress(self, var, scope):
        if var in self.functions[scope]['values']:
            return self.functions[scope]['values'][var]['dir']
        elif var in self.functions['global']['values']:
            return self.functions['global']['values'][var]['dir']        
        else:
            return False

    def lookupFunctionType(self, func):
        return self.functions[func]["tipo"]
    
    def lookupArrObj(self, var, scope):
        if var in self.functions[scope]['values']:
            if 'arrObj' in self.functions[scope]['values'][var]:
                return self.functions[scope]['values'][var]['arrObj']
            else:
                raise Exception("Var ", var, " is not an array")
        elif var in self.functions['global']['values']:
            if 'arrObj' in self.functions[scope]['values'][var]:
                return self.functions[scope]['values'][var]['arrObj']
            else:
                raise Exception("Var ", var, " is not an array")
        else:
            raise Exception("Var ", var, " not declared")

    def lookupIsArray(self, var,scope):
        if var in self.functions[scope]['values']:
            if 'arrObj' in self.functions[scope]['values'][var]:
                raise Exception("Var ", var, " is an array")
        elif var in self.functions['global']['values']:
            if 'arrObj' in self.functions[scope]['values'][var]:
                raise Exception("Var ", var, " is an array")

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
            raise Exception("Not compatible", varA, tipoA, varB, tipoB)
    
