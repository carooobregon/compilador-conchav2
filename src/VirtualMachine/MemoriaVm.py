class MemoriaVM:
    def __init__(self, memoryIdx):
        self.enteros = [0 for i in range(memoryIdx[2])]
        self.flotantes = [0 for i in range(memoryIdx[3])]
        self.booleanos = [0 for i in range(memoryIdx[4])]
        self.strings = [0 for i in range(memoryIdx[4])]
        self.tempI = [0 for i in range(memoryIdx[7])]
        self.tempF = [0 for i in range(memoryIdx[8])]
        self.tempB = [0 for i in range (memoryIdx[9])]
        self.offset = 1000 if memoryIdx[0] == 'global' else 2000
        pass

    ## para acceder, se resta el offset del scope o se checa si es temp
    ## tiene q hacer una funcion que cheque en que rango esta
