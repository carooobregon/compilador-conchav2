import pprint

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
                                    "cantT" : ""}}
    
    def addFunction(self, funcInfo, name):
        # self.declareFuncInFuncTable()
        print(funcInfo)
        self.funcTable[name] = {
                                "tipo": funcInfo["tipo"],
                                "dirV": funcInfo["quadCounter"],
                                "cantI": funcInfo["varCounter"][0],
                                "cantF": funcInfo["varCounter"][1],
                                "cantB": funcInfo["varCounter"][2],
                                "cantS": funcInfo["varCounter"][3],
                                "cantVar" : funcInfo["tempVars"],
                                "totalVars" : funcInfo["varCounter"][0] + funcInfo["varCounter"][1] + funcInfo["varCounter"][2] + funcInfo["varCounter"][3] + funcInfo["tempVars"]

                            }
    
    def getAttribute(self, name, attr):
        return self.funcTable[name][attr]
    
    def printFunctionTable(self):
        print("FUNCTION TABLE")
        pp.pprint(self.funcTable)