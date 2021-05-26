from Utils.Stack import Stack
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs
from Utils.Queue import Queue

class QuadReloaded:

    pilaTipos = Stack()
    pilaJumps = Stack()
    filaPrincipal = Queue()
    ut = UtilFuncs()
    pendientesJumps = Stack()

    def __init__(self):
        pass
    
    def pushQuadArithmeticQueue(self, a, temp, const, var, scope):
        a = a.items
        for i in a:
            cont = 0
            while(cont < len(i)):
                i[cont] = self.lookUpMemoryVal(temp, const, var, i[cont], scope)
                cont += 1
            self.filaPrincipal.push(i)
    
    def lookUpMemoryVal(self, temp, const, var, val, scope):
        # if var.lookupVariableAddress(val, scope):
        #     return var.lookupVariableAddress(val, scope)
        # elif const.lookupConstantAddress(val):
        #     return const.lookupConstantAddress(val)
        # elif temp.lookupTempAddress(val):
        #     return temp.lookupTempAddress(val)
        # elif self.symbolMemoryVal(val):
        #     return self.symbolMemoryVal(val)
        return val

    def symbolMemoryVal(self, sym):
        if sym == 'SUM':
            return 1
        elif sym == 'SUB':
            return 2
        elif sym == 'MUL':
            return 3
        elif sym == 'DIV':
            return 4
        elif sym == '=':
            return 5
        elif sym == '<':
            return 6
        elif sym == '>':
            return 7
        elif sym == '!=':
            return 8
        elif sym == '==':
            return 9
        elif sym == 'GOTO' or sym == 'GoTo':
            return 10
        elif sym == 'GotoF':
            return 11
        elif sym == 'END':
            return 12
        elif sym == 'PARAMETER':
            return 13
        elif sym == 'write':
            return 14
        elif sym == 'ENDFUNC':
            return 15
        elif sym == 'ERA':
            return 16
        elif sym == 'GOSUB':
            return 17
        elif sym == 'RETURN':
            return 18

 # TODO: completar esto jsjsf
    def parsePrint(self,p, temp, const, var, scope):
        p = self.lookUpMemoryVal(temp, const, var, p, scope)
        self.filaPrincipal.push([14, p])
    
    def printFilaPrincipal(self):
        print("FILA PRINCIPAL")
        cont = 0 
        for i in self.filaPrincipal.items:
            print(cont+1,i)
            cont += 1
        print("FIN PRINCIPAL")
    
    def pushFilaPrincipal(self, a, temp, const, var, scope):
        cont = 0
        while(cont < len(a)):
            a[cont] = self.lookUpMemoryVal(temp, const, var, a[cont], scope)
            cont+=1
        self.filaPrincipal.push(a)
    
    def pushListFilaPrincipal(self, a, temp, const, var, scope):
        for i in a:
            print("DEBUGG", i)
            cont = 0
            while(cont < len(i)):
                i[cont] = self.lookUpMemoryVal(temp, const, var, i[cont], scope)
                cont += 1
            self.filaPrincipal.push(i)

    def pushJumpPendiente(self):
        self.pendientesJumps.push(self.filaPrincipal.size()-1)

    def pushJumpPendienteSize(self):
        self.pendientesJumps.push(self.filaPrincipal.size())

    def pushJumpFirstWhile(self):
        self.pendientesJumps.push(self.filaPrincipal.size()+1)

    def updateJumpPendiente(self):
        self.filaPrincipal.items[self.pendientesJumps.peek()][1] = self.filaPrincipal.size()+1
        self.pendientesJumps.pop()

    def finWhile(self):
        end = self.pendientesJumps.pop()
        ret = self.pendientesJumps.pop()
        self.filaPrincipal.items.append(["Goto", ret])
        self.filaPrincipal.items[end-1][1] = self.filaPrincipal.size()+1
    
    def currPrincipalCounter(self):
        return self.filaPrincipal.size()
    
    def updateFirstGoto(self):
        self.filaPrincipal.items[0][1] = self.filaPrincipal.size()+1