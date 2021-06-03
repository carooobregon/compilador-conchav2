# UtilFuncs is a library that stores helper functions that can be used throughout the directory

from Parser.Arreglo import ArregloNodo
from Parser.Stack import Stack
from Parser.Queue import Queue
from Parser.TempTable import TempObject

import copy

class UtilFuncs:
    funcStack = Stack()

    def __init__(self):
        self.currParams = []
        pass

    # Flatten is used to make a single list out of many nested lists
    def flatten(self,miLista):
        if miLista == []:
            return miLista
        if isinstance(miLista[0], list):
            return self.flatten(miLista[0]) + self.flatten(miLista[1:])
        return miLista[:1] + self.flatten(miLista[1:])

    # Merges two dictionaries together
    def mergeDictionaries(self, dict1, dict2):
        return(dict2.update(dict1))
    
    # Converts types into a more conventional way we use throughout compiler
    def convertTypes(self, tipo):
        if(tipo == 'entero') or tipo == 'INT' or isinstance(tipo, int):
            return "INT"
        if(tipo == 'flotante') or tipo == 'FLOT' or isinstance(tipo, float):
            return "FLOT"
        if(tipo == 'ID'):
            return "ID"
        if(tipo == 'cadena') or tipo == 'STR' or isinstance(tipo, str):
            return "STR"
        if(tipo == 'booleano') or tipo == 'BOOL' or isinstance(tipo, bool):
            return "BOOL"
        if isinstance(tipo, TempObject) or isinstance(tipo, ArregloNodo):
            return tipo.type
        return tipo.gettokentype()
    
    # Gets value of element
    def getValue(self, val):
        t = type(val)
        if isinstance(val, int):
            return val
        elif isinstance(val,float):
            return val
        elif isinstance(val, str):
            return val
        elif isinstance(val, bool):
            return val
        elif isinstance(val, TempObject) or isinstance(val, ArregloNodo):
            return val
        else:
            t = (type(val))
            return val.value

    # Handles print statements to generate the appropiate quadruples, evaluates expressions using evaluateQuadruple
    # if there's arithmetic in the current list of items to print
    def handlePrintStatements(self, lista, st, currentScope, currGlobal, quadreload, qd, temp, mem, const):
        for i in lista:
            i = self.flatten(i)
            fin = ""
            if(len(i) > 1):
                nuevaQ, currTemp, quadType = qd.evaluateQuadruple(i, st, currentScope, currGlobal)
                temp.transformTemps(nuevaQ.items,mem)
                currGlobal = currTemp
                quadreload.pushQuadArithmeticQueue(nuevaQ, temp, const, st, currentScope)
                fin = nuevaQ.tail()[3]
                qd.clearQueue()
            else:
                fin = self.getValue(i[0])
            quadreload.parsePrint(fin, temp, const, st, currentScope)
        return currGlobal

    # Resets various counters when a scope finishes
    def finishFunc(self, st, currGlobal, currentScope, mem, funcTable):
        st.addTempVars(currGlobal, currentScope)
        funcInfo = st.getFunctionInfo(currentScope)
        tempCounters = mem.getTemps()
        funcTable.addFunction(funcInfo, currentScope, tempCounters)
        mem.resetLocal()
        currGlobal = 0
        currTempN = 1
        return currGlobal, currTempN, funcTable, mem
