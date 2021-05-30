import pprint
import numpy as np

## TODO separate temps by type
pp = pprint.PrettyPrinter(indent = 4)
class FunctionTable:
    def __init__(self):
        self.funcTable = {"global": {
                                    "tipo": "np",
                                    "dirV": "-999",
                                    "cantI": "",
                                    "cantF": "",
                                    "cantB": "",
                                    "cantS": "",
                                    "cantT" : "",
                                    'cantVarI' : 20,
                                    'cantVarF' : 20,
                                    'cantVarB' : 20, 
                                    'cantVarS' : 20}}
    
    def addFunction(self, funcInfo, name, tempVals):
        # self.declareFuncInFuncTable()
        self.funcTable[name] = {
                                "tipo": funcInfo["tipo"],
                                "dirV": funcInfo["quadCounter"],
                                "cantI": funcInfo["varCounter"][0],
                                "cantF": funcInfo["varCounter"][1],
                                "cantB": funcInfo["varCounter"][2],
                                "cantS": funcInfo["varCounter"][3],
                                "cantVar" : funcInfo["tempVars"],
                                "totalVars" : funcInfo["varCounter"][0] + funcInfo["varCounter"][1] + funcInfo["varCounter"][2] + funcInfo["varCounter"][3] + funcInfo["tempVars"],
                                'cantVarI' : tempVals[0],
                                'cantVarF' : tempVals[1],
                                'cantVarB' : tempVals[2],
                                'cantVarS' : tempVals[3]
                            }
    
    def getAttribute(self, name, attr):
        return self.funcTable[name][attr]
    
    def printFunctionTable(self):
        print("FUNCTION TABLE")
        pp.pprint(self.funcTable)
    def exportFunctionTable(self):
        a = np.array(self.transformFunctionTableToArray())
        print("ARR BEFORE CSV", a, type(a))
        np.savetxt('funcTable.csv', a, delimiter=',', fmt="%s")

    def transformFunctionTableToArray(self):
        final = []
        for i in self.funcTable: 
            curr = []
            curr.append(i)
            i = self.funcTable[i]
            curr.append(i["tipo"])
            curr.append(i["dirV"])
            curr.append(i["cantI"])
            curr.append(i["cantF"])
            curr.append(i["cantB"])
            curr.append(i["cantS"])
            curr.append(i["cantVar"])
            curr.append(i["totalVars"])
            curr.append(i["cantVarI"])
            curr.append(i["cantVarF"])
            curr.append(i["cantVarB"])
            curr.append(i["cantVarS"])
            print(curr)
            final.append(curr)
        print("FINAL", final)
        return final
    
    def setDirVGloval(self, dirV):
        self.funcTable["global"]["dirV"] = dirV