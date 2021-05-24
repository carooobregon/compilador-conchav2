import pprint

pp = pprint.PrettyPrinter(indent = 4)

class ConstantTable():
    def __init__(self):
        self.constTable = {}
        self.currCounter = 0

    def add(self, elem):
        if elem not in self.constTable:
            self.constTable[elem] = self.currCounter

    def lookup(self, elem):
        if elem not in self.constTable:
            self.add(elem)
            self.currCounter += 1
        return self.constTable[elem]

    def printConst(self):
        print("Constant Table")
        pp.pprint(self.constTable)