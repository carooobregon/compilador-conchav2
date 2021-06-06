from numpy.core.fromnumeric import var
import rply
from rply import ParserGenerator
from Parser.symbolTable import SymbolTable
from Parser.semantic import SemanticCube
from Parser.UtilFuncs import UtilFuncs
from Parser.quadruples import Quadruple
from Parser.Stack import Stack
from Parser.Queue import Queue
from Parser.QuadReloaded import QuadReloaded
from Parser.ParamHandler import ParamHandler
from Parser.Memoria import Memoria
from Parser.functionTable import FunctionTable
from Parser.constantTable import ConstantTable
from Parser.TempTable import TempTable
from Parser.TempTable import TempObject
from Parser.Arreglo import Arreglo, ArregloNodo
import numpy as np

import pprint
import copy
pp = pprint.PrettyPrinter(indent=4)

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['PROGRAMA', 'IF', 'ELSE', 'PRINT', 'WHILE', 'INT', 'STR', 'FLOT', 'LPARENS',
            'RPARENS', 'LKEY', 'RKEY', 'SUM', 'SUB','MUL', 'DIV', 'EQ', 'COMM', 'PTOCOM', 
            'MOTHN', 'LETHN', 'NEQ', 'CORCH_LEFT', 'CORCH_RIGHT', 'CORCH_LEFT',
            'FOR', 'FUNCION', 'VACIO', 'ID', 'STRING', 'LPARENS', 'RPARENS', 'CTE_ENT', 
            'CTE_FLOAT','BOOLEANO', 'EQUALITY', 'VERDADERO', 'FALSO', 'PRINCIPAL', 
            'VAR', 'COLON', 'RETURN','READ','CLASS','OBJ','INCLUDE'
            ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV'])
            ]
        )
        self.qd = Quadruple()
        self.reloadQuad = QuadReloaded()
        self.st = SymbolTable()
        self.ut = UtilFuncs()
        self.scopeStack = Stack()
        self.sCube = SemanticCube()
        self.paramH = ParamHandler(self.st)
        self.mem = Memoria()
        self.funcTable = FunctionTable()
        self.constantTable = ConstantTable()
        self.tempTable = TempTable()
        # self.arregloNodo = ArregloNodo()
        self.currParm = []
        self.tempWrite = []
        self.tempRead = []
        self.currentScope= "global"
        self.callingFunc = ""
        self.currGlobal = 0
        self.resWh = TempObject("temp", "temp")
        self.dirToRet = ""
        self.hasRet = 0
        self.classTable = {}
        self.classScope = ""
        self.currArr = ""

    def parse(self):
        # Last function to run, exports all the quadruple stack into a csv file that can be read in the virtual machine
        @self.pg.production('empezando : clase  programa')
        @self.pg.production('empezando :  programa')
        def expression_empezando(p):
            a = np.array(self.reloadQuad.getFilaPrincipal())
            np.savetxt('CompilationFiles/quadruples.csv', a, delimiter=',', fmt="%s")
            return p
        
        # Finishes populating the global scope information and exports function and constant table of the whole program 
        @self.pg.production('programa :  include PROGRAMA startbkpoint ID PTOCOM many_vars prog_aux_func start_main principal_driver  ')
        @self.pg.production('programa :  include PROGRAMA startbkpoint ID PTOCOM many_vars start_main principal_driver ')
        @self.pg.production('programa :   PROGRAMA startbkpoint ID PTOCOM many_vars prog_aux_func start_main principal_driver')
        @self.pg.production('programa :   PROGRAMA startbkpoint ID PTOCOM many_vars start_main principal_driver')
        def expression_programa(p):
            self.reloadQuad.pushFilaPrincipal(["END"], self.tempTable, self.constantTable, self.st, self.currentScope)
            self.st.addTempVars(self.currGlobal, "global")
            tempCounters = self.mem.getTemps()
            self.funcTable.addFunction(self.st.getFunctionInfo("global"), "global", tempCounters)
            self.funcTable.exportFunctionTable()
            self.constantTable.exportConstantTable()

            self.reloadQuad.printFilaPrincipal()
            return p

        #Declares a class
        @self.pg.production('clase : clasegetid  many_obj prog_aux_func  RKEY  PTOCOM')
        @self.pg.production('clase : clasegetid many_obj  RKEY  PTOCOM ')
        def expression_clase(p):
            plana = self.ut.flatten(p)
            self.classScope = plana[1].value
            self.reloadQuad.pushFilaPrincipal(["END"], self.tempTable, self.constantTable, self.st, self.currentScope)
            self.st.addTempVars(self.currGlobal,"global")
            tempCounters = self.mem.getTemps()
            self.funcTable.addFunction(self.st.getFunctionInfo("global"), ("class "  + plana[1].value),tempCounters)
            self.funcTable.exportFunctionTable()
            self.constantTable.exportConstantTable()
            return p

        @self.pg.production('clasegetid : CLASS  ID  startClassBkpoint LKEY  ')
        def expression_clase(p):
            self.classScope = p[1].value
            self.classTable[p[1].value] = {"cadena":[],"entero":[],"flotante":[], "booleano":[]}
            return p
        
        @self.pg.production('include : INCLUDE ID PTOCOM ')
        def expression_indluce(p): 
            return p
        
        @self.pg.production('startClassBkpoint : ')
        def expression_startClassBkpoint(p):
            self.reloadQuad.pushFilaPrincipal(["GOTO", ""], self.tempTable, self.constantTable, self.st, self.currentScope)
            return p

        # Pushes first GOTO into the quad stack to point to the counter where main starts
        @self.pg.production('startbkpoint : ')
        def expression_progauxfunc(p):
            self.reloadQuad.pushFilaPrincipal(["GOTO", ""], self.tempTable, self.constantTable, self.st, self.currentScope)
            return p

        @self.pg.production('prog_aux_func : func prog_aux_func')
        @self.pg.production('prog_aux_func : func')
        def expression_progauxfunc(p):
            return p

        @self.pg.production('principal_driver : PRINCIPAL LPARENS RPARENS principal_bkpoint func_bloque ')
        def expression_progauxfunc(p):
            return p
        
        @self.pg.production('principal_bkpoint : ')
        def expression_progauxfunc(p):
            self.currentScope = "global"
            return p

        @self.pg.production('varsObj : VAR varsAuxA COLON tipo PTOCOM')
        @self.pg.production('varsObj : VAR varsAuxA COLON miobj')
        def expression_addingvar(p):
            plana = self.ut.flatten(p)
            if plana[3].gettokentype() == "INT":
                self.classTable[self.classScope]["entero"].append(plana[1].value)
            elif plana[3].gettokentype() =="FLOT":
                self.classTable[self.classScope]["flotante"].append(plana[1].value)
            elif plana[3].gettokentype() =="STR":
                self.classTable[self.classScope]["cadena"].append(plana[1].value)
            else:
                self.classTable[self.classScope]["booleano"].append(plana[1].value)
            return p
        @self.pg.production('many_obj : varsObj many_obj')
        @self.pg.production('many_obj : varsObj')
        @self.pg.production('many_obj : ')
        def expression_progauxfunc(p):
            return p

        @self.pg.production('varsObj : VAR varsAuxA COLON tipo PTOCOM')
        @self.pg.production('varsObj : VAR varsAuxA COLON miobj')
        def expression_addingvar(p):
            plana = self.ut.flatten(p)
            if plana[3].gettokentype() == "INT":
                self.classTable[self.classScope]["entero"].append(plana[1].value)
            elif plana[3].gettokentype() =="FLOT":
                self.classTable[self.classScope]["flotante"].append(plana[1].value)
            elif plana[3].gettokentype() =="STR":
                self.classTable[self.classScope]["cadena"].append(plana[1].value)
            else:
                self.classTable[self.classScope]["booleano"].append(plana[1].value)
            return p
        # Recursive grammar to receive many vars

        @self.pg.production('many_vars : vars many_vars')
        @self.pg.production('many_vars : vars')
        @self.pg.production('many_vars : ')
        def expression_progauxfunc(p):
            return p

        @self.pg.production('miobj : ID LPARENS RPARENS PTOCOM')
        def expression_miobj(p):
            return p
        
        # Processes vars and adds them to symbol table
        @self.pg.production('vars : VAR varsAuxA COLON tipo PTOCOM')
        @self.pg.production('vars : VAR varsAuxA COLON miobj')
        def expression_addingvar(p):
            plana = self.ut.flatten(p)
            if plana[4].gettokentype() =='LPARENS':
                temp = self.classTable[plana[3].value]["entero"]
                for i in temp:
                    tempN = i[0].upper() + i[1:]
                    self.st.processObjVars((plana[1].value + tempN),"INT",self.currentScope,self.mem)
                temp = self.classTable[plana[3].value]["flotante"]
                for i in temp:
                    tempN = i[0].upper() + i[1:]
                    self.st.processObjVars((plana[1].value+tempN),"FLOT",self.currentScope,self.mem)
                temp = self.classTable[plana[3].value]["cadena"]
                for i in temp:
                    tempN = i[0].upper() + i[1:]
                    self.st.processObjVars((plana[1].value+tempN),"STR",self.currentScope,self.mem)
                temp = self.classTable[plana[3].value]["booleano"]
                for i in temp:
                    tempN = i[0].upper() + i[1:]
                    self.st.processObjVars((plana[1].value+tempN),"BOOL",self.currentScope,self.mem)
            else:
                self.st.processVars(p[1], p[3], self.currentScope, self.mem)
            # print("uhhhh hello?", p)
            return p

        @self.pg.production('varsAuxA : varType COMM varsAuxA')
        @self.pg.production('varsAuxA : varType')
        def expression_addingvar(p):
            return p

        @self.pg.production('varType : arrDecl')
        def expression_addingarr(p):
            return p[0]

        @self.pg.production('varType : ID')
        def expression_addingvar(p):
            return p

        @self.pg.production('arrDecl : arrbkpid many_dims')
        def varsArr(p):
            # plana = self.ut.flatten(p)
            # if len(plana) <= 4: # arr  de 1 dim
            #     dim1 = int(plana[2].value)
            #     elArr = np.full(dim1,0)
            #     print("arr declar", elArr)
            # else:
            #     dim1 = int(plana[2].value)
            #     dim2 = int(plana[5].value)
            #     elArr = np.full((dim1,dim2),0)
            #     print("arr muldim", elArr)
            cop = copy.deepcopy(self.currArr)
            # print("deep copy boi", cop)
            return cop
        # Grammar to receive array declaration
        @self.pg.production('many_dims : optDimDeclare optDimDeclare')
        @self.pg.production('many_dims : optDimDeclare')
        def manydimsprod(p):
            return

        # Adds dimension node to array
        @self.pg.production('optDimDeclare : CORCH_LEFT CTE_ENT CORCH_RIGHT')
        def declProd(p):
            print("declarando arr", p)
            self.currArr.addNode(int(p[1].value))
            # self.arregloNodo.calculoElda(p[1].value)
            return 
        
        # Starts new array object
        @self.pg.production('arrbkpid : ID')
        def expression_tipo(p):
            nuevoArr = Arreglo(p[0].value)
            self.currArr = nuevoArr
            return p[0] 

        @self.pg.production('tipo : INT')
        @self.pg.production('tipo : FLOT')
        @self.pg.production('tipo : STR')
        @self.pg.production('tipo : BOOLEANO')
        def expression_tipo(p):
            return p[0]
        # Updates first goto and sets virtual dimension of global on fucntiontable 
        @self.pg.production('start_main : ')
        def expression_progauxfunc(p):
            dir = self.reloadQuad.updateFirstGoto()
            self.funcTable.setDirVGloval(dir)
            return p

        # Processes return of function, validates is the same type and performs quadruples if it needs it
        @self.pg.production('retorno : RETURN expresion PTOCOM')
        def expression_return(p):
            self.hasRet = 1
            plana = self.ut.flatten(p[1])

            funcRet = self.st.lookupFunctionType(self.currentScope)
            retType = ""
            arg = ""
            if(len(plana) > 1):
                nuevaQ, currTemp, quadType = self.qd.evaluateQuadruple(plana, self.st, self.currentScope,self.currGlobal)
                self.currGlobal = currTemp
                nuevaQ.items = self.tempTable.transformTemps(nuevaQ.items, self.mem)
                self.currGlobal = currTemp
                self.reloadQuad.pushQuadArithmeticQueue(nuevaQ, self.tempTable, self.constantTable, self.st, self.currentScope)
                arg = nuevaQ.tail()[3]
                retType = quadType
                self.qd.clearQueue()
            else:
                retType = self.ut.convertTypes(plana[0]) if self.ut.convertTypes(plana[0]) != 'ID' else self.st.lookupType(plana[0].value, self.currentScope)
                arg = self.ut.getValue(plana[0])
            if retType != funcRet:
                raise Exception("Invalid return, was expecting", funcRet, "and got", retType, "instead")
        
            add = self.st.lookupVariableAddress(self.callingFunc, "global")
            self.reloadQuad.pushFilaPrincipal(["RETURN", arg, add], self.tempTable, self.constantTable, self.st, self.currentScope)
            self.reloadQuad.pushGoToRet()
            return p
            
        @self.pg.production('func_bloque : LKEY bloqaux RKEY PTOCOM')
        def expression_fun_bloque(p):
            return p[1]

        @self.pg.production('bloque : LKEY bloqaux RKEY')
        def expression_bloque(p):
            return p[1]

        @self.pg.production('bloqaux : estatuto bloqaux')
        @self.pg.production('bloqaux : estatuto')
        def expression_bloqaux(p):
            return p

        # Update return jumps, push to main quad ENDFUNC, makes sure function returned something
        @self.pg.production('func : FUNCION func_declaraux func_bkpoint RKEY PTOCOM endFunc')
        def expression_funcnoret(p):
            funcTipo = self.st.lookupFunctionType(self.callingFunc)
            if funcTipo != 'vacio' and not self.hasRet :
                raise Exception("Was expecting", self.callingFunc, "to return var of type", funcTipo)
            self.reloadQuad.pushFilaPrincipal(["ENDFUNC"], self.tempTable, self.constantTable, self.st, self.currentScope)
            self.reloadQuad.updateRetJumps()
            self.currGlobal, self.currTempN, self.funcTable, self.mem = self.ut.finishFunc(self.st, self.currGlobal, self.currentScope, self.mem, self.funcTable)
            return p

        @self.pg.production('func_bkpoint : many_vars LKEY bloqaux')
        def expression_declarauxvacio(p):
            return p

        # Grammar to receive function call declaration
        @self.pg.production('func_declaraux : VACIO ID LPARENS parms RPARENS')
        @self.pg.production('func_declaraux : tipo ID LPARENS parms RPARENS')
        def expression_declaraux(p):
            self.callingFunc = p[1].value
            self.st.processFuncDeclP(p[:4], self.mem)
            self.currentScope = p[1].value
            self.st.addQuadCounterFunc(self.reloadQuad.currPrincipalCounter(), self.currentScope)
            return p

        @self.pg.production('endFunc : ')
        def expression_params(p):

            return p

        @self.pg.production('parms : tipo ID COMM parms')
        @self.pg.production('parms : tipo ID')
        @self.pg.production('parms : ')
        def expression_params(p):
            return p
            
        @self.pg.production('estatuto : call_func PTOCOM')
        @self.pg.production('estatuto : asignacion')
        @self.pg.production('estatuto : condicion')
        @self.pg.production('estatuto : escritura')
        @self.pg.production('estatuto : ciclo')
        @self.pg.production('estatuto : retorno')
        def expression_estatuto(p):
            return p

        # Grammar to process function call, processes parameters, creates a GOSUB
        @self.pg.production('call_func : bkpt_callfunc1 LPARENS call_func_aux RPARENS')
        def expression_callfunc(p):
            c = self.callingFunc
            tipo = self.st.lookupFunctionType(c)
            params = self.paramH.handleParams(self.st.getParams(c), self.st, self.currentScope ,self.currGlobal, self.currParm)
            self.currParm = []
            params = self.tempTable.transformTemps(params,  self.mem)
            self.reloadQuad.pushListFilaPrincipal(params, self.tempTable, self.constantTable, self.st, self.currentScope)
            initAddress = self.st.lookupquadCounter(self.callingFunc)
            self.reloadQuad.pushFuncSymListaP(["GOSUB", self.callingFunc, initAddress])
            res = -999
            if tipo != "vacio":
                address = self.st.lookupVariableAddress(self.callingFunc, "global")
                res = TempObject(self.st.lookupType(self.callingFunc, "global"), self.currentScope)
                self.tempTable.addSingleVar(res, self.mem)
                self.reloadQuad.pushFilaPrincipal(["=", address, res], self.tempTable, self.constantTable, self.st, self.currentScope)
            return res

        # Starts function by pushing function to symbol table and updates callingfunc variable to the function that's being called
        @self.pg.production('bkpt_callfunc1 : ID ')
        def expression_callfunc(p):
            self.st.lookupFunction(p[0].value)
            name = p[0].value.replace('\'', '')
            self.reloadQuad.pushFuncSymListaP(["ERA", name])
            self.callingFunc = p[0].value
            return p
        
        # Inserts parms into currparms list to process in handleParams
        @self.pg.production('call_func_aux : accepted_params COMM call_func_aux')
        @self.pg.production('call_func_aux : accepted_params')
        def expression_callfuncaux(p):
            self.currParm.insert(0,p[0])
            return p

        @self.pg.production('accepted_params : expresion')
        @self.pg.production('accepted_params : STRING')
        def expression_acceptedparams(p):
            return p

        @self.pg.production('ciclo : wh_loop')
        def expression_ciclo(p):
            return p

        # Calls the reloadQuad function finWhile to process the finish of whille and add pending jumps to quadruple stack
        @self.pg.production('wh_loop : WHILE bktCondWhile cond_body bktAfterCondW bktWhile bloque')
        def expression_whloop(p):
            self.reloadQuad.finWhile()
            return p
    
        # Pushes first jump condition to quad stack
        @self.pg.production('bktCondWhile : ')
        def expression_bktcondwhile(p):
            self.reloadQuad.pushJumpFirstWhile()

        # Pushes gotof and adds temporal object to temptable so memory instance can be created
        @self.pg.production('bktWhile : ')
        def expression_bktwhile(p):
            self.tempTable.addSingleVar(self.resWh, self.mem)
            self.reloadQuad.pushFilaPrincipal(["GotoF", "", self.resWh], self.tempTable, self.constantTable, self.st, self.currentScope)
            self.resWh = TempObject("temp", "temp")

        # Pushes jump to quadruple stack
        @self.pg.production('bktAfterCondW : ')
        def expresspktfinwhile(p):
            self.reloadQuad.pushJumpFirstWhile()
            return p

        @self.pg.production('asignable_elems : call_arrval')
        def expression_declaracion(p): 
            return p

        @self.pg.production('asignable_elems : ID')
        def expression_declaracion(p): 
            return p

        # Verifies type of and variable of left side variable and generates quadruple
        # to memory
        @self.pg.production('asignacion : asignable_elems EQ ID PTOCOM') #a[X]= / a = a; a[X]= string/a = string;
        @self.pg.production('asignacion : asignable_elems EQ STRING PTOCOM')
        def expresion_asignacion_arithm(p):
            ret = ""
            p[0] = p[0][0]

            if isinstance(p[0], ArregloNodo):
                var1Val = self.st.lookupVar(p[0].name, self.currentScope)
                var1Type = self.st.lookupType(p[0].name, self.currentScope)
                ret = p[0]
            else:
                self.st.lookupIsArray(p[0].value, self.currentScope)
                var1Val = self.st.lookupVar(p[0].value, self.currentScope)
                var1Type = self.st.lookupType(p[0].value, self.currentScope)
                ret = p[0].value
                
            if(p[2].gettokentype() == "STRING"):
                self.constantTable.add(str(p[2].value), self.mem)
                self.reloadQuad.pushFilaPrincipal(["=", p[2].value, ret], self.tempTable, self.constantTable, self.st, self.currentScope)
            else:
                var2Val = self.st.lookupVar(p[2].value, self.currentScope)
                var2Type = self.st.lookupType(p[2].value, self.currentScope)
                
                tipoOp = self.sCube.validateType(var1Type, var2Type)
                if tipoOp != 'ERR':
                    self.reloadQuad.pushFilaPrincipal(["=", p[2].value, ret], self.tempTable, self.constantTable, self.st, self.currentScope)               
            return p

        @self.pg.production('asignacion : asignable_elems EQ READ LPARENS RPARENS PTOCOM')
        def expresion_asignacion_lectura(p):
            self.reloadQuad.pushFilaPrincipal(["lectura",p[0][0].value],self.tempTable,self.constantTable, self.st, self.currentScope)
            return p

        # Verifies type and that first variable exists and generated quadruples for left side variable 
        @self.pg.production('asignacion : asign_op PTOCOM')
        def expresion_asignacionog(p):
            plana = self.ut.flatten(p)
            if isinstance(plana[0], ArregloNodo):
                var1Val = self.st.lookupVar(plana[0].name, self.currentScope)
                var1Type = self.st.lookupType(plana[0].name, self.currentScope)
                ret = plana[0]
            else:
                var1Val = self.st.lookupVar(plana[0].value, self.currentScope)
                var1Type = self.st.lookupType(plana[0].value, self.currentScope)
                ret = var1Val
            if(len(plana) == 4):
                if isinstance(plana[2], TempObject) or isinstance(plana[2], ArregloNodo):
                    var2Val = plana[2]
                    var2Type = plana[2].type
                elif isinstance(plana[2], float) or isinstance(plana[2], int) or  isinstance(plana[2], bool) or  isinstance(plana[2], str):
                    var2Val = plana[2]
                    var2Type = type(plana[2])
                else:
                    var2Val = plana[2].value
                    var2Type = self.st.lookupType(plana[2].value, self.currentScope)
                self.reloadQuad.pushFilaPrincipal(["=", var2Val, ret], self.tempTable, self.constantTable, self.st, self.currentScope)
            else:
                nuevaQ, currTemp, quadType = self.qd.evaluateQuadruple(plana[2:], self.st, self.currentScope,self.currGlobal)
                var2Val = nuevaQ.top()[3]
                tipoOp = self.sCube.validateType(var1Type, quadType)
                self.currGlobal = currTemp
                if tipoOp != 'ERR':
                    nuevaQ.items = self.tempTable.transformTemps(nuevaQ.items,  self.mem)
                    self.currGlobal = currTemp
                    self.reloadQuad.pushQuadArithmeticQueue(nuevaQ, self.tempTable, self.constantTable, self.st, self.currentScope)
                    arg = nuevaQ.tail()[3]
                    self.reloadQuad.pushFilaPrincipal(["=", arg, ret], self.tempTable, self.constantTable, self.st, self.currentScope)
                    self.qd.clearQueue()
            return p

        @self.pg.production('asign_op : asignable_elems EQ expresion')
        def expresion_asignacion(p):
            return p

        # Prints contents of print statement using the help of util funcs' handleprintstatements function
        @self.pg.production('escritura : PRINT LPARENS esc_aux_helper RPARENS PTOCOM')
        def expression_escritura(p):
            self.currGlobal = self.ut.handlePrintStatements(self.tempWrite, self.st, self.currentScope, self.currGlobal, self.reloadQuad, self.qd, self.tempTable, self.mem, self.constantTable)
            self.tempWrite = []
            return p

        # Flattens elements in the body of print statement
        @self.pg.production('esc_aux_helper : escaux esc_aux_helper')
        @self.pg.production('esc_aux_helper : escaux')
        def expression_progauxfunc(p):
            plana = self.ut.flatten(p[0])
            self.tempWrite.insert(0, plana)
            return p

        @self.pg.production('escaux : expresion COMM')
        @self.pg.production('escaux : expresion')
        def print_strings(p):
            return p[0]

        @self.pg.production('expresion : expresion_comp')
        @self.pg.production('expresion : exp')
        def expression_expresion(p):
            return p
        
        # Generates quads to evaluate comparison expressions
        @self.pg.production('expresion_comp : exp EQUALITY exp')
        @self.pg.production('expresion_comp : exp MOTHN exp')
        @self.pg.production('expresion_comp : exp LETHN exp')
        @self.pg.production('expresion_comp : exp NEQ exp')
        def expression_expcomp(p):
            primeraParte = self.ut.flatten(p[0])
            segundaParte = self.ut.flatten(p[2])
            val,valType, val2 , val2Type = [0 for _ in range(4)]

            if(len(primeraParte) > 1):
                nuevaQ1, currTemp, valType = self.qd.evaluateQuadruple(primeraParte,self.st, self.currentScope,self.currGlobal)
                nuevaQ1.items = self.tempTable.transformTemps(nuevaQ1.items,  self.mem)
                self.currGlobal = currTemp
                self.reloadQuad.pushQuadArithmeticQueue(nuevaQ1, self.tempTable, self.constantTable, self.st, self.currentScope)
                val = nuevaQ1.top()[3]
                self.qd.clearQueue()
            else:
                val = primeraParte[0]
                valType = self.ut.convertTypes(primeraParte[0])
                if(valType == 'ID'):
                    valType = self.st.lookupType(val.value, self.currentScope)

            if(len(segundaParte) > 1):
                nuevaQ2, currTemp, val2Type = self.qd.evaluateQuadruple(segundaParte,self.st, self.currentScope,self.currGlobal)
                nuevaQ2.items = self.tempTable.transformTemps(nuevaQ2.items, self.mem)
                self.reloadQuad.pushQuadArithmeticQueue(nuevaQ2, self.tempTable, self.constantTable, self.st, self.currentScope)
                val2 = nuevaQ2.top()[3]
                self.currGlobal = currTemp
                self.qd.clearQueue()
            else:
                val2 = segundaParte[0]
                val2Type = self.ut.convertTypes(segundaParte[0])
                if(val2Type == 'ID'):
                    val2Type = self.st.lookupType(val2.value, self.currentScope)

            isBool = self.sCube.validateOperationBool(valType, val2Type)
            self.currGlobal += 1
            if(isBool):
                res = TempObject("BOOL", self.currGlobal)
                self.tempTable.addSingleVar(res, self.mem)
                self.reloadQuad.pushFilaPrincipal([p[1].value, self.ut.getValue(val), self.ut.getValue(val2), res], self.tempTable, self.constantTable, self.st, self.currentScope)
            else:
                raise Exception("!!", val, "cannot be compared to", val2, "!!")
            self.resWh = res
            return res
                    
        @self.pg.production('condicion : IF cond_body gotof bloque cond_aux fincond')
        def expression_condicion(p):
            return p
        
        # Updates pending jump that sits currently in stack
        @self.pg.production('fincond : ')
        def bkpoint_gotof(p):
            self.reloadQuad.updateJumpPendiente()

        # Handles gotoF 
        @self.pg.production('gotof : ')
        def bkpoint_gotof(p):
            self.tempTable.addSingleVar(self.resWh, self.mem)
            self.reloadQuad.pushFilaPrincipal(["GotoF", "", self.resWh], self.tempTable, self.constantTable, self.st, self.currentScope)
            self.reloadQuad.pushJumpPendiente()

        @self.pg.production('cond_body : LPARENS expresion_comp RPARENS')
        def expression_condBody(p):
            return p[1] 

        @self.pg.production('cond_aux : ELSE bkpointelse bloque PTOCOM')
        @self.pg.production('cond_aux : PTOCOM')
        def expression_condAux(p):
            return p

        @self.pg.production('bkpointelse : ')
        def expression_condAux(p):
            self.reloadQuad.pushFilaPrincipal(["Goto", ""], self.tempTable, self.constantTable, self.st, self.currentScope)
            self.reloadQuad.updateJumpPendiente()
            self.reloadQuad.pushJumpPendiente()
            return p

        @self.pg.production('exp : termino SUM exp')
        @self.pg.production('exp : termino SUB exp')
        @self.pg.production('exp : termino')
        def expression_exp(p):
            return p

        @self.pg.production('termino : factor MUL termino')
        @self.pg.production('termino : factor DIV termino')
        @self.pg.production('termino : factor')
        def expression_termino(p):
            return p

        @self.pg.production('factor : left_paren expresion RPARENS')
        @self.pg.production('factor : SUM constante')
        @self.pg.production('factor : SUB constante')
        @self.pg.production('factor : constante')
        def expression_factor(p):
            return p

        # Raises exception if function is not supposed to return value
        @self.pg.production('constante : call_func')
        def expression_callfunc(p):
            if p[0] == -999:
                raise Exception("Function " , self.callingFunc, " doesn't return value")
            return p[0]

        # Crea arreglo nodo 2D
        @self.pg.production('call_arrval : ID CORCH_LEFT exp CORCH_RIGHT CORCH_LEFT exp CORCH_RIGHT') 
        def constma(p):
            nodo = ArregloNodo(p[0].value, [p[2].value, p[5].value], 2, self.st.lookupVariableAddress(p[0].value, self.currentScope), self.st.lookupType(p[0].value, self.currentScope), self.st.lookupArrObj(p[0].value, self.currentScope))
            return nodo

        # Crea arreglo nodo 1D
        @self.pg.production('call_arrval : ID CORCH_LEFT exp CORCH_RIGHT') 
        def constarr(p):
            plana = self.ut.flatten(p[2])#aqui solo es para cuando se indexa el arr
            if len(plana) == 1: 
                if isinstance(plana[0], int):
                    nodo = ArregloNodo(p[0].value, p[2], 1, self.st.lookupVariableAddress(p[0].value, self.currentScope), self.st.lookupType(p[0].value, self.currentScope), self.st.lookupArrObj(p[0].value, self.currentScope), self.st.lookupVariableAddress(p[0].value, self.currentScope) + plana[0])
                else:
                    res = TempObject("", "")
                    self.tempTable.addSingleVar(res, self.mem)
                    dirMemTemp = self.tempTable.lookupTempAddress(res)
                    self.reloadQuad.pushFilaPrincipal(["ARRADD", plana[0].value, self.st.lookupVariableAddress(p[0].value, self.currentScope), dirMemTemp], self.tempTable, self.constantTable, self.st, self.currentScope)
                    addr = self.st.lookupVariableAddress(p[0].value, self.currentScope)
                    nodo =  ArregloNodo(p[0].value, addr, 1, self.st.lookupVariableAddress(p[0].value, self.currentScope), self.st.lookupType(p[0].value, self.currentScope), self.st.lookupArrObj(p[0].value, self.currentScope), dirMemTemp)
            else:
                nuevaQ, currTemp, quadType = self.qd.evaluateQuadruple(plana, self.st, self.currentScope,self.currGlobal)
                self.currGlobal = currTemp
                nuevaQ.items = self.tempTable.transformTemps(nuevaQ.items, self.mem)
                self.currGlobal = currTemp
                self.reloadQuad.pushQuadArithmeticQueue(nuevaQ, self.tempTable, self.constantTable, self.st, self.currentScope)
                arg = nuevaQ.tail()[3]
                self.qd.clearQueue()
##             ["ARRADD", arg, basememory, res]
## manejar scopes de tempobj en vm
                res = TempObject("", "")
                self.tempTable.addSingleVar(res, self.mem)
                dirMemTemp = self.tempTable.lookupTempAddress(res)
                addr = self.st.lookupVariableAddress(p[0].value, self.currentScope)
                nodo =  ArregloNodo(p[0].value, addr, 1, self.st.lookupVariableAddress(p[0].value, self.currentScope), self.st.lookupType(p[0].value, self.currentScope), self.st.lookupArrObj(p[0].value, self.currentScope), dirMemTemp)
                self.reloadQuad.pushFilaPrincipal(["ARRADD", arg, self.st.lookupVariableAddress(p[0].value, self.currentScope), dirMemTemp], self.tempTable, self.constantTable, self.st, self.currentScope)
            return nodo

        @self.pg.production('constante : call_arrval')
        @self.pg.production('constante : ID')
        @self.pg.production('constante : VERDADERO')
        @self.pg.production('constante : FALSO')
        @self.pg.production('constante : numero')
        def expression_constante(p):
            return p
            
        @self.pg.production('constante : STRING') 
        @self.pg.production('constante : OBJ') 
        def expression_string(p):
            self.constantTable.add(str(p[0].value), self.mem)
            return p


        # Retorna el valor de numero NO TOKEN
        @self.pg.production('numero : CTE_FLOAT')
        @self.pg.production('numero : CTE_ENT')
        def expresion_numero(p):
            # print( "soi el numero ", p)
            if p[0].gettokentype() == 'CTE_FLOAT':
                self.constantTable.add(float(p[0].value), self.mem)
                return float(p[0].value)
            elif p[0].gettokentype() == 'CTE_ENT':
                self.constantTable.add(int(p[0].value), self.mem)
                return int(p[0].value) 

        @self.pg.production('left_paren : LPARENS')
        def expresion_parens(p):
            return p[0].value

        @self.pg.error
        def error_handler(token):
            raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype(), token)

    def get_parser(self):
        return self.pg.build()