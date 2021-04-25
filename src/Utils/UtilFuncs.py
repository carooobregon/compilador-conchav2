import queue
from Utils.symbolTable import SymbolTable

class UtilFuncs:
    def __init__(self):
        self.functionNameQ = queue.Queue()
    
    def addFunctionNameQ(self, f, sym, currNo):
        self.functionNameQ.put(f)
        print("q", list(self.functionNameQ.queue))

class Params:
    params = []

    def __init__(self, pars):
        this.params = pars
        pass

    def processParams(self):
        print("self.params)