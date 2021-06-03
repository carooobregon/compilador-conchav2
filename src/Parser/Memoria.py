# Memoria is a helper class that helps concha compiler keep track of the current memory counters within scopes
# and variable types

class Memoria:
    def __init__(self):
        self.baseScopes = [1000, 2000, 3000, 4000]
        self.offset = [0, 250, 500, 750]
        self.maxN = 250
        self.allMemory = self.initMemory()
        self.mapaMemoria = {}

    def addVar(self, scope, type):
        return self.addVarMemory(self.getScopeForMemory(scope), self.getIdxForMemory(type))
    
    def initMemory(self):
        globalScope = [1000, 1250, 1500, 1750]
        local = [2000, 2250, 2500, 2750]
        temporal = [3000, 3250, 3500, 3750]
        constante =[4000, 4250, 4500, 4750]
        return [globalScope, local, temporal, constante]

    def getIdxForMemory(self, type):
        if type == 'INT' or isinstance(type, int):
            return 0
        elif type == 'FLOT' or isinstance(type, float):
            return 1
        elif type == 'BOOL' or isinstance(type, bool) :
            return 2
        elif type == 'STR' or isinstance(type, str):
            return 3
        
    def getScopeForMemory(self, scope):
        if scope == 'global':
            return 0
        elif scope == 'temporal':
            return 2
        elif scope == 'constante':
            return 3
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
        self.allMemory[1] = [2000, 2250, 2500, 2750]
        self.allMemory[2] = [3000, 3250, 3500, 3750]
    
    def getTemps(self):            
        return [self.allMemory[2][0] - 3000, self.allMemory[2][1] - 3250, self.allMemory[2][2] - 3500, self.allMemory[2][3] - 3750]
    
    def addArray(self, arr, type, scope):
        sz = arr.size
        first = self.addVarMemory(self.getScopeForMemory(scope), self.getIdxForMemory(type))
        for i in range(sz - 1):
            self.addVarMemory(self.getScopeForMemory(scope), self.getIdxForMemory(type))
        return first