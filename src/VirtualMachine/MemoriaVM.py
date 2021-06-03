class MemoriaVM:
    RANGES = [0, 250, 500, 750]
    def __init__(self, memoryIdx, nombre):
        self.enteros = [0 for i in range(memoryIdx[2])]
        self.flotantes = [0 for i in range(memoryIdx[3])]
        self.booleanos = [0 for i in range(15)]
        self.strings = [0 for i in range(15)]
        self.tempI = [0 for i in range(memoryIdx[8])]
        self.tempF = [0 for i in range(memoryIdx[9])]
        self.tempB = [0 for i in range (memoryIdx[10])]
        self.tempS = [0 for i in range(memoryIdx[11])]
        self.offset = 1000 if nombre == 'global' else 2000
        
    def asignElement(self, address, valor):
        if address >= 3000:
            self.assignTempElement(address, valor)
        else:
            self.assignLookupScopesElement(address, valor) 
    
    def assignLookupScopesElement(self, address, valor):
        add = address % self.offset
        if add < self.RANGES[1]:
            self.enteros[add] = valor
            return

        if add < self.RANGES[2]:
            self.flotantes[add % self.RANGES[1]] = valor
            return

        if add < self.RANGES[3]:
            print("index out of range ", add, self.RANGES, add % self.RANGES[2])
            self.booleanos[add % self.RANGES[2]] = valor
            return
        else:
            self.strings[add % self.RANGES[3]] = valor
            return
        
    def assignTempElement(self, address, valor):
        add = address % 3000
        if add < self.RANGES[1]:
            self.tempI[add] = valor

        elif add < self.RANGES[2]:
            self.tempF[add % self.RANGES[1] ] = valor

        elif add < self.RANGES[3]:
            self.tempB[add % self.RANGES[2]] = valor
        else:
            self.tempS[add % self.RANGES[3]] = valor

    def lookupElement(self, address):
        if address >= 3000:
            return self.lookupTempElement(address)
        else:
            return self.lookupScopesElement(address)
    
    def lookupScopesElement(self, address):
        add = address % self.offset
        if add < self.RANGES[1]:
            return self.enteros[add]

        if add < self.RANGES[2]:
            return self.flotantes[add % self.RANGES[1]]

        if add < self.RANGES[3]:
            return self.booleanos[add % self.RANGES[2]]
        else:
            return self.strings[add % self.RANGES[3]]

    def lookupTempElement(self, address):
        add = address % 3000
        if add < self.RANGES[1]:
            return self.tempI[add]
        if add < self.RANGES[2] :
            return self.tempF[add % self.RANGES[1]]

        if add < self.RANGES[3]:
            return self.tempB[add % self.RANGES[2]]
        else:
            return self.tempS[add % self.RANGES[3]]

    def printElements(self,obj):
        print("enteros")
        print(obj.enteros)
        print("flotantes")
        print(obj.flotantes)
        print("booleanos")
        print(obj.booleanos)
        print("strings")
        print(obj.strings)
        print("tempI")
        print(obj.tempI)
        print("tempF")
        print(obj.tempF)
        print("tempB")
        print(obj.tempB)
        print("tempS")
        print(obj.tempS)
        print("offset")
        print(obj.offset)
