from rply import ParserGenerator
import pprint
import copy

pp = pprint.PrettyPrinter(indent=4)

class SymbolTable:
    def __init__(self):
        self.functions={}
        self.currentScope ={}
        self.currFuncNum = 0
    
    def addVarCurrScope(self, var):
        if(len(var) < 4):
            self.currentScope[var[1].value] = [var[0].value]
        else:
            self.currentScope[var[1].value] = ["arr_" + var[0].value]
        print("currsco", self.currentScope)
    
    def closeCurrScope(self, f):
        self.functions[0] = copy.deepcopy(self.currentScope)
        self.currentScope.clear()
        print("Func ", self.functions)
        print("Current ", self.currentScope)
        self.currFuncNum+= 1
    
    def printSymbolTable(self):
        pp.pprint(self.functions)

    def replaceKey(self, name):
        self.functions[name] = self.functions.pop(0)