import pprint
pp = pprint.PrettyPrinter(indent = 4)
class TempTable():
    SCOPE = 'temporal'
    def __init__(self):
        self.tempTable = {}

    def add(self, elem, memory):
        if elem not in self.tempTable:
            self.tempTable[elem] = memory.addVar(self.SCOPE, elem)

    def lookupTempAddress(self, elem):
        if elem in self.tempTable:
            return self.tempTable[elem]
        return False

    def printConst(self):
        print("Temp Table")
        pp.pprint(self.tempTable)

    def transformTemps(self, q, mem):
        for i in q:
            count = 0
            while(count < len(i)):
                if isinstance(i[count], str) and i[count][0] == "t":
                    self.add(i[count], mem)
                count += 1
        return q