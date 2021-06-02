import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent = 4)
class ConstantTable():
    SCOPE = 'constante'
    def __init__(self):
        self.constTable = []

    def add(self, elem, memory):
        if elem not in self.constTable:
            self.constTable.append(elem)

    def lookupConstantAddress(self, elem):
        if elem in self.constTable:
            return self.constTable.index(elem) + 4000
        else:
            return False

    def printConst(self):
        print("Constant Table")
        pp.pprint(self.constTable)

    def exportConstantTable(self):
        data = self.constTable
        a = np.array(data)
        np.savetxt('constTable.csv', a, delimiter=',', fmt="%s")