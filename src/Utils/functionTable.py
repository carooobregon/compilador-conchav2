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
    
    def addFunction(self, funcInfo):

        self.funcTable[name]["tipo"] = funcInfo["tipo"]
        self.funcTable[name]["dirV"] = funcInfo["quadCounter"]
        self.funcTable[name]["cantI"] = funcInfo["localvars"]
        # self.funcTable[name]["cantF"] = funcInfo[""]
        # self.funcTable[name]["cantB"] = cantB
        # self.funcTable[name]["cantS"] = cantS
        # self.funcTable[name]["cantT"] = cantT
    
    def getAttribute(self, name, attr):
        return self.funcTable[name][attr]
