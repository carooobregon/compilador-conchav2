from Utils.Stack import Stack
from Utils.Queue import Queue
from Utils.UtilFuncs import UtilFuncs
from Utils.quadruples import Quadruple

import copy

class ParamHandler:

    def __init__(self):
        self.ut = UtilFuncs()
        self.qd = Quadruple()
    
    def updateVals(self, paramsNeeded, st, scope, currGlobal):
        self.processedParams = []
        self.params = paramsNeeded
        self.ut = UtilFuncs()
        self.currParm = 0
        self.st = st
        self.currentScope = scope
        self.qd = Quadruple()
        self.currGlobal = currGlobal

    def clearVals(self):
        self.processedParams = []
        self.params = []
        self.currParm = []
        self.st = []
        self.currentScope = []
        self.currGlobal = []

    def handleParams(self, paramsNeeded, st, scope, currGlobal, p):
        self.updateVals(paramsNeeded, st, scope, currGlobal)
        for i in p:
            self.paramHandler(i)
        parms = copy.deepcopy(self.processedParams)
        self.clearVals()
        return parms

    def paramHandler(self, p):
        plana = []
        if isinstance(p, list):
            plana = self.ut.flatten(p)
        else:
            plana = [p[0]]
        arg = ""
        accessParm = len(self.params) - self.currParm-1
        if(self.currParm+1 > len(self.params)):
            raise Exception("more params than expected", len(self.params))
        if(len(plana) == 1):
            arg = self.handleSoloParam(plana)
        else:
            arg = self.handleQuadParam(plana)
        
        self.processedParams.append(["PARAMETER", arg, "param" + str(self.currParm+1)])
        self.currParm += 1

    def handleSoloParam(self,plana):
        soloparm = self.ut.convertTypes(plana[0])
        arg = self.ut.getValue(plana[0])
        if(soloparm == 'ID'):
            soloparm = self.st.lookupType(plana[0].value, self.currentScope)
        if(self.ut.convertTypes(soloparm) != self.params[self.currParm]):
            raise Exception("!! different param type !! ", soloparm, " expected ", self.params[self.currParm])
        return arg
    
    def handleQuadParam(self, plana):
        q, currTemp, quadType = self.qd.evaluateQuadruple(plana,self.st, self.currentScope,self.currGlobal)
        nuevaQ = copy.deepcopy(q)
        arg = "t" + str(currTemp)
        self.qd.clearQueue()
        self.currGlobal = currTemp
        self.pushQuadArithmeticQueue(nuevaQ)
        if(self.ut.convertTypes(quadType) != self.params[self.currParm]):
            raise Exception("!! different param type !! ", quadType, " expected ", self.params[self.currParm])
        return arg

    def getProcessedParams(self):
        return self.processedParams

    def pushQuadArithmeticQueue(self, q):
        for i in q.items:
            self.processedParams.append(i)