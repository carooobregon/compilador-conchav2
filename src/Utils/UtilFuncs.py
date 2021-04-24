import queue
from Utils.symbolTable import SymbolTable

class UtilFuncs:
    params = []
    def __init__(self):
        self.functionNameQ = queue.Queue()
    
    def addFunctionNameQ(self, f, sym, currNo):
        self.functionNameQ.put(f)
        print("q", list(self.functionNameQ.queue))