import pprint
import numpy as np

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
                                    'cantVarI' : "",
                                    'cantVarF' : "",
                                    'cantVarB' : '' }}
    
    def addFunction(self, funcInfo, name):
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
                                'cantVarI' : "",
                                'cantVarF' : "",
                                'cantVarB' : '' 
                            }
    
    def getAttribute(self, name, attr):
        return self.funcTable[name][attr]
    
    def printFunctionTable(self):
        print("FUNCTION TABLE")
        pp.pprint(self.funcTable)
    
    def exportFunctionTable(self):
        a = np.array(self.transformFunctionTableToArray())
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
            print(curr)
            final.append(curr)
        print("FINAL", final)
        return final