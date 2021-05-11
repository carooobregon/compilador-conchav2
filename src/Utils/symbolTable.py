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
        self.functions={"global" : {"values" : {}}}
        self.currentScope ={}
        self.currFuncNum = 0
        self.functionNameQ = queue.Queue()
        self.st = SemanticCube()

    # ADD FUNCTIONS

    def addVarNormalScope(self, varName, scope, varType):
        self.functions[scope]["values"][varName] = {"tipo" : varType}
    
    def declareFuncInSymbolTable(self,p):
        self.functions[p[2].value] = {"tipo" : p[0].value, "values" : {}}

    # PROCESSING FUNCTIONS    
    def processVars(self,vars, tipo, scope):
        plana = self.util.flatten(vars)
        for i in plana:
            if(i.value != ','):
                self.functions[scope]["values"][i.value] = {"tipo" : tipo}

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
            self.functions[p[2].value][listaParams[cont+1].value] = {"tipo": listaParams[cont].gettokentype()}
            cont +=3

    def closeCurrScope(self, funcName, funcRet):
        finalVals = copy.deepcopy(self.currentScope)
        if funcName in self.functions:
            self.util.mergeDictionaries(self.functions[funcName], finalVals)
        self.functions[funcName] = {"values" : finalVals, "tipo" : funcRet}
        # self.currentScope.clear()
        self.currFuncNum+= 1
    
    # LOOKUP FUNCTIONS
    def lookupType(self,nombreVar, scope):
        currScopeVals = self.functions[scope]
        if nombreVar in currScopeVals:
            return currScopeVals[nombreVar]["tipo"]
        else:
            raise Exception("!! EXC Variable", nombreVar, "not declared", "scope", scope, "!!")
    
    def lookupVar(self,nombreVar, scope):
        currScopeVals = self.functions[scope]['values']
        if nombreVar in currScopeVals:
            return nombreVar
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