import pprint

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
        self.funcTable[name] = {
                                "tipo": funcInfo["tipo"],
                                "dirV": funcInfo["quadCounter"],
                                "cantI": funcInfo["varCounter"][0],
                                "cantF": funcInfo["varCounter"][1],
                                "cantB": funcInfo["varCounter"][2],
                                "cantS": funcInfo["varCounter"][3],
                            }
    
    def getAttribute(self, name, attr):
        return self.funcTable[name][attr]
