class constantTable():
    def __init__(self):
        self.constTable = {}
        self.currCounter = 0

    def addConstTable(self, elem):
        self.constTable[elem] = self.currCounter

    def lookUpConstTable(self, elem):
        if elem not in self.constTable:
            self.addConstTable(elem)
        return self.constTable[elem]