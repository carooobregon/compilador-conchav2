import pprint

pp = pprint.PrettyPrinter(indent = 4)
class ConstantTable():
    SCOPE = 'constante'
    def __init__(self):
        self.constTable = {}

    def add(self, elem, memory):
        if elem not in self.constTable:
            self.constTable[elem] = memory.addVar(self.SCOPE, elem)

    def lookupConstantAddress(self, elem):
        if elem in self.constTable:
            return self.constTable[elem]
        return False

    def printConst(self):
        print("Constant Table")
        pp.pprint(self.constTable)