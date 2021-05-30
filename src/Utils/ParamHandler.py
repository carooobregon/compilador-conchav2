from Utils.Stack import Stack
from Utils.Queue import Queue
from Utils.UtilFuncs import UtilFuncs
from Utils.quadruples import Quadruple
from Utils.TempTable import TempObject

import copy

class ParamHandler:
    listaParams = []
    count = 0
    orderedParms = []
    flatParms = []
    params = []
    scope = ""
    util = UtilFuncs()
    memoria = ""
    currI = 2000
    currF = 2250
    currB = 2500
    currS = 2750

    def __init__(self, st):
        self.ut = UtilFuncs()
        self.qd = Quadruple()
        self.st = st
    
    def updateVals(self, paramsNeeded, st, scope, currGlobal):
        self.processedParams = []
        self.params = paramsNeeded
        self.ut = UtilFuncs()
        self.currParm = 0
        self.st = st
        self.currentScope = scope
        self.qd = Quadruple()
        self.currGlobal = currGlobal
        self.listaParams = []
        self.count = 0
        self.orderedParms = []
        self.flatParms = []


    def clearVals(self):
        self.processedParams = []
        self.params = []
        self.currParm = 0
        self.st = []
        self.currentScope = []
        self.currGlobal = []
        self.currI = 2000
        self.currF = 2250
        self.currB = 2500
        self.currS = 2750


    def handleParams(self, paramsNeeded, st, scope, currGlobal, p):
        self.updateVals(paramsNeeded, st, scope, currGlobal)
        for i in p:
            arg, type = self.paramHandler(i)
            self.processedParams.append(["PARAMETER", arg, self.getParamMemoryAddress(type)])
        parms = copy.deepcopy(self.processedParams)
        self.clearVals()
        return parms

    def getParamMemoryAddress(self, type):
        if type == 'INT' or isinstance(type, int):
            currA = self.currI
            self.currI += 1
            return currA
        elif type == 'FLOT' or isinstance(type, float):
            currA = self.currF
            self.currF += 1
            return currA
        elif type == 'BOOL' or isinstance(type, bool) :
            currA = self.currB
            self.currB += 1
            return currA
        elif type == 'STR' or isinstance(type, str):
            currA = self.currS
            self.currS += 1
            return currA

    def paramHandler(self, p):
        plana = []
        if isinstance(p, list):
            plana = self.ut.flatten(p)
        else:
            plana = [p[0]]
        arg = ""
        type = ""
        accessParm = len(self.params) - self.currParm-1
        if(self.currParm+1 > len(self.params)):
            raise Exception("more params than expected", len(self.params), "handler")
        if(len(plana) == 1):
            arg, type = self.handleSoloParam(plana)
        else:
            arg, type = self.handleQuadParam(plana)
        self.currParm += 1
        return arg, type

    def handleSoloParam(self,plana):
        soloparm = self.ut.convertTypes(plana[0])
        arg = self.ut.getValue(plana[0])
        if(soloparm == 'ID'):
            soloparm = self.st.lookupType(plana[0].value, self.currentScope)
        if(self.ut.convertTypes(soloparm) != self.params[self.currParm]):
            raise Exception("!! different param type !! ", soloparm, " expected ", self.params[self.currParm])
        return arg, self.ut.convertTypes(soloparm)
    
    def handleQuadParam(self, plana):
        q, currTemp, quadType = self.qd.evaluateQuadruple(plana,self.st, self.currentScope,self.currGlobal)
        nuevaQ = copy.deepcopy(q)
        # arg = "t" + str(currTemp)
        self.qd.clearQueue()
        self.currGlobal = currTemp
        self.pushQuadArithmeticQueue(nuevaQ)
        
        if(self.ut.convertTypes(quadType) != self.params[self.currParm]):
            raise Exception("!! different param type !! ", quadType, " expected ", self.params[self.currParm])
        return nuevaQ.tail()[3], quadType

    def getProcessedParams(self):
        return self.processedParams

    def pushQuadArithmeticQueue(self, q):
        for i in q.items:
            self.processedParams.append(i)

    def updateParamObj(self, params, scope, st, memoria):
        self.memoria = memoria
        self.params = params
        self.scope = scope
        self.st = st
        self.util = UtilFuncs()
        self.addParamsLista()
        self.listaParams = []

    def addParamsLista(self):
        self.orderedParms = []
        self.createListParams()
        cont = 0
        while cont < len(self.listaParams)-1:
            currTipo = self.listaParams[cont].gettokentype()
            currDir = self.memoria.addVar(self.scope, currTipo)
            self.st.functions[self.scope]["values"][self.listaParams[cont+1].value] = {"tipo": currTipo, "dir" : currDir}
            self.st.functions[self.scope]["varCounter"][self.memoria.getIdxForMemory(currTipo)] += 1
            # self.st.functions[self.scope]["localvars"] += 1
            cont +=3

    def createListParams(self):
        self.st.functions[self.scope]["parms"] = []
        self.getListaParams()
        self.st.functions[self.scope]["parms"] = self.orderedParms

    def getListaParams(self):
        if len(self.params) < 3:
            self.procesSingleParam()
        else:
            self.processManyParams()

    def procesSingleParam(self):
        count = 0
        self.addListaparams()
        self.orderedParms.append(self.util.convertTypes(self.flatparms[0].value))
        count +=3

    def processManyParams(self):
        count = 0
        for i in self.params:
            if isinstance(i, list):
                self.listaParams = self.util.flatten(i)
        self.listaParams.append(',')
        self.addListaparams()
        while(count < len(self.flatparms)):
            self.orderedParms.append(self.util.convertTypes(self.flatparms[count].value))
            count +=3 

    def addListaparams(self):
        self.listaParams.append(self.params[0])
        self.listaParams.append(self.params[1])
        self.flatparms = self.util.flatten(self.params)