from Utils.Stack import Stack
from Utils.Queue import Queue
from Utils.UtilFuncs import UtilFuncs
from Utils.quadruples import Quadruple

import copy

class ParamHandler:

    def __init__(self, paramsNeeded, st, scope, qd, currGlobal, reloadQuad):
        self.processedParams = []
        self.params = paramsNeeded
        self.ut = UtilFuncs()
        self.currParm = 0
        self.st = st
        self.currentScope = scope
        self.qd = Quadruple()
        self.currGlobal = currGlobal
        self.reloadQuad =reloadQuad
        # self.functionNameQ = Queue()
    
    def paramHandler(self, p):
        plana = []
        print("TYPE", p, type(p))
        if isinstance(p, list):
            plana = self.ut.flatten(p)
        else:
            plana = [p[0]]
        arg = ""
        accessParm = len(self.params) - self.currParm-1
        print("currparm", self.currParm, plana[0], plana)
        if(self.currParm+1 > len(self.params)):
            raise Exception("more params than expected", len(self.params))

        if(len(plana) == 1):
            soloparm = self.ut.convertTypes(plana[0])
            arg = self.ut.getValue(plana[0])
            # arg = plana[]
            if(soloparm == 'ID'):
                soloparm = self.st.lookupType(plana[0].value, self.currentScope)
            if(self.ut.convertTypes(soloparm) != self.params[self.currParm]):
                raise Exception("!! different param type !! ", soloparm, " expected ", self.params[self.currParm])
        else:
            q, currTemp, quadType = self.qd.evaluateQuadruple(plana,self.st, self.currentScope,self.currGlobal)
            nuevaQ = copy.deepcopy(q)
            arg = "t" + str(currTemp)
            self.qd.clearQueue()
            self.currGlobal = currTemp
            self.reloadQuad.pushQuadArithmeticQueue(nuevaQ)
            print("mytype", quadType)
            print(accessParm)
            if(self.ut.convertTypes(quadType) != self.params[self.currParm]):
                raise Exception("!! different param type !! ", quadType, " expected ", self.params[self.currParm])
        # self.reloadQuad.pushFilaPrincipal(["PARAMETER", arg, "param" + str(self.currParm+1)])
        
        self.reloadQuad.pushFilaPrincipal(["PARAMETER", arg, "param" + str(self.currParm+1)])
        self.currParm += 1