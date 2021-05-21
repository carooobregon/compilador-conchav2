import copy

class Memoria:
    def __init__(self):
        ## global 0, local 1, temp 2, const 3
        self.baseScopes = [1000, 2000, 3000, 4000]
        self.offset = [0, 250, 500, 750]
        self.maxN = 250
        self.globalScope = [1000, 1250, 1500, 1750]
        self.local = [2000, 2250, 2500, 2750]
        self.temporal = [3000, 3250, 3500, 3750]
        self.constante =[4000, 4240, 4500, 4750]
        self.allMemory = [self.globalScope, self.local, self.temporal, self.constante]
        self.mapaMemoria = {}

    def addVar(self, scope, type):
        return self.addVarMemory(self.getScopeForMemory(scope), self.getIdxForMemory(type))
    
    def getIdxForMemory(self, type):
        if type == 'INT':
            return 0
        elif type == 'FLOT':
            return 1
        elif type == 'BOOL':
            return 2
        elif type == 'STRING':
            return 3
    
    def getScopeForMemory(self, scope):
        if scope == 'global':
            return 0
        else:
            return 1

    def addVarMemory(self, scope, type):
        address = self.allMemory[scope][type]
        if(address < self.baseScopes[scope] + self.offset[type] + self.maxN):
            self.mapaMemoria[address] = -9999
            self.sumVar(scope, type)
            return address
        else:
            raise Exception("Too many vars of type", type, "in ", scope, " scope")

    def sumVar(self, scope, type):
        self.allMemory[scope][type] += 1

    def resetLocal(self):
        self.local = [2000, 2250, 2500, 2750]