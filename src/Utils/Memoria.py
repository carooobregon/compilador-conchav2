class Memoria:
    def __init__(self):
        self.baseGlobal = 1000
        self.baseLocal = 2000
        self.baseTemporal = 3000
        self.baseConstante = 4000
        self.offset = [0, 250, 500, 750]
        self.maxN = 250
        self.globalScope = [1000, 1250, 1500, 1750]
        self.local = [2000, 2250, 2500, 2750]
        self.temporal = [3000, 3250, 3500, 3750]
        self.constante =[4000, 4240, 4500, 4750]
        self.mapaMemoria = {}

    def addGlobal(self, idx):
        temp = self.getGlobal(idx)
        if(temp < self.baseGlobal + self.offset + self.maxN):
            self.sumGlobal(idx)
            self.mapaMemoria[temp] = -9999
        else:
            Exception("Too many vars in global scope")
        return temp

    def addTemporal(self, idx):
        temp = self.getTemporal(idx)
        self.sumTemporal(idx)
        return temp

    def addLocal(self, idx):
        temp = self.getLocal(idx)
        self.sumLocal(idx)
        return temp

    def addConstante(self, idx):
        temp = self.getCte(idx)
        self.sumLocal(idx)
        return temp

    def getGlobal(self, idx):    
        return self.globalScope[idx]
    
    def getTemporal(self, idx):
        return self.temporal[idx]
        
    def getLocal(self,idx):
        return self.local[idx]

    def getCte(self,idx):
        return self.constante[idx]
    
    def sumGlobal(self, idx):
        self.globalScope[idx] += 1
    
    def sumTemporal(self, idx):
        self.temporal[idx] += 1

    def sumConstante(self, idx):
        self.constante[idx] += 1

    def sumLocal(self, idx):
        self.local[idx] += 1

    def resetLocal(self):
        self.local = [2000, 2250, 2500, 2750]
    
    def getIdxForMemory(self, type):
        if type == 'INT':
            return 0
        elif type == 'FLOT':
            return 1
        elif type == 'BOOL':
            return 2
        elif type == 'STRING':
            return 3
    
    def addVar(self, scope, idx):
        if scope == 'global':
            return self.addGlobal(idx)
        else:
            return self.addLocal(idx)