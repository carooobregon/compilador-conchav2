##TODOS 
# Separar la function table de la var table
# Hacer los counters para tipos de variables
# cambiar que lo q se pngan en los quads sea la direccion
# quitar que las variables globales se agreguen a cada funcion
# hacer clase memoria (un humilde mapa)
# ir pensando en 0bj*t0s

import rply
from rply import ParserGenerator
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs
from Utils.quadruples import Quadruple
from Utils.Stack import Stack
from Utils.Queue import Queue
from Utils.QuadReloaded import QuadReloaded
from Utils.ParamHandler import ParamHandler
from Utils.Memoria import Memoria
from Utils.functionTable import FunctionTable
from Utils.ConstantTable import ConstantTable
from Utils.TempTable import TempTable
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
            'VAR', 'COLON', 'RETURN'
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
        self.currParm = []
        self.tempWrite = []
        self.currentScope= "global"
        self.callingFunc = ""
        self.currGlobal = 0


    def parse(self):
        @self.pg.production('empezando : programa')
        def expression_empezando(p):
            a = np.array(self.reloadQuad.getFilaPrincipal())
            np.savetxt('quadruples.csv', a, delimiter=',', fmt="%s")
            return p

        @self.pg.production('programa : PROGRAMA startbkpoint ID PTOCOM many_vars prog_aux_func start_main principal_driver')
        @self.pg.production('programa : PROGRAMA startbkpoint ID PTOCOM many_vars start_main principal_driver')
        def expression_programa(p):
            self.reloadQuad.pushFilaPrincipal(["END"], self.tempTable, self.constantTable, self.st, self.currentScope)
            self.st.addTempVars(self.currGlobal, "global")
            self.funcTable.addFunction(self.st.getFunctionInfo("global"), "global")
            self.st.printSt()
            self.reloadQuad.printFilaPrincipal()
            self.funcTable.printFunctionTable()
            self.constantTable.printConst()
            return p

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

        @self.pg.production('many_vars : vars many_vars')
        @self.pg.production('many_vars : vars')
        @self.pg.production('many_vars : ')
        def expression_progauxfunc(p):
            return p

        # @self.pg.production('declarar_main : declare_vars PTOCOM')
        @self.pg.production('vars : VAR varsAuxA COLON tipo PTOCOM')
        def expression_addingvar(p):
            # print("adding", p[1], self.currentScope)
            self.st.processVars(p[1], p[3], self.currentScope, self.mem)
            return p

        @self.pg.production('varsAuxA : ID COMM varsAuxA')
        @self.pg.production('varsAuxA : ID')
        def expression_addingvar(p):
            return p

        @self.pg.production('tipo : INT')
        @self.pg.production('tipo : FLOT')
        @self.pg.production('tipo : STR')
        @self.pg.production('tipo : BOOLEANO')
        def expression_tipo(p):
            return p[0]
        
        @self.pg.production('start_main : ')
        def expression_progauxfunc(p):
            self.reloadQuad.updateFirstGoto()
            # self.reloadQuad.pushFilaPrincipal(["GOTO", ""], self.tempTable, self.constantTable, self.st, self.currentScope)
            return p

        @self.pg.production('retorno : RETURN expresion PTOCOM')
        def expression_return(p):
            plana = self.ut.flatten(p[1])
            funcRet = self.st.lookupFunctionType(self.currentScope)
            if(len(plana) > 1):
                raise Exception("Invalid return")
            retVal = self.ut.convertTypes(plana[0]) if self.ut.convertTypes(plana[0]) != 'ID' else self.st.lookupType(plana[0].value, self.currentScope)
            if retVal != funcRet:
                raise Exception("Invalid return, was expecting", funcRet, "and got", retVal, "instead")
            self.reloadQuad.pushFilaPrincipal(["RETURN"], self.tempTable, self.constantTable, self.st, self.currentScope)
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

        @self.pg.production('func : FUNCION func_declaraux_vacio func_bkpoint RKEY PTOCOM endFunc')
        @self.pg.production('func : FUNCION func_declaraux func_bkpoint retorno RKEY PTOCOM endFunc')
        def expression_func(p):
            self.st.addTempVars(self.currGlobal, self.currentScope)
            funcInfo = self.st.getFunctionInfo(self.currentScope)
            self.funcTable.addFunction(funcInfo, self.currentScope)
            self.mem.resetLocal()
            self.currGlobal = 0
            self.currTempN = 1
            return p

        @self.pg.production('func_bkpoint : many_vars LKEY bloqaux')
        def expression_declarauxvacio(p):
            return p

        @self.pg.production('func_declaraux_vacio : VACIO ID LPARENS parms RPARENS')
        @self.pg.production('func_declaraux : tipo ID LPARENS parms RPARENS')
        def expression_declaraux(p):
            self.st.processFuncDeclP(p[:4], self.mem)
            self.currentScope = p[1].value
            self.st.addQuadCounterFunc(self.reloadQuad.currPrincipalCounter(), self.currentScope)
            return p

        @self.pg.production('endFunc : ')
        def expression_params(p):
            self.reloadQuad.pushFilaPrincipal(["ENDFUNC"], self.tempTable, self.constantTable, self.st, self.currentScope)

            return p

        @self.pg.production('parms : tipo ID COMM parms')
        @self.pg.production('parms : tipo ID')
        @self.pg.production('parms : ')
        def expression_params(p):
            return p
            
        @self.pg.production('estatuto : call_func')
        @self.pg.production('estatuto : declaracion')
        @self.pg.production('estatuto : asignacion')
        @self.pg.production('estatuto : condicion')
        @self.pg.production('estatuto : escritura')
        @self.pg.production('estatuto : ciclo')
        @self.pg.production('estatuto : test_grammar')
        def expression_estatuto(p):
            print(p)
            return p

        @self.pg.production('call_func : bkpt_callfunc1 LPARENS call_func_aux RPARENS PTOCOM')
        def expression_callfunc(p):
            c = self.callingFunc
            params = self.paramH.handleParams(self.st.getParams(c), self.st, self.currentScope ,self.currGlobal, self.currParm)
            self.currParm = []
            params = self.tempTable.transformTemps(params,  self.mem)
            self.reloadQuad.pushListFilaPrincipal(params, self.tempTable, self.constantTable, self.st, self.currentScope)
            initAddress = self.st.lookupquadCounter(self.callingFunc)
            self.reloadQuad.pushFilaPrincipal(["GOSUB", self.callingFunc, initAddress], self.tempTable, self.constantTable, self.st, self.currentScope)
            return p

        @self.pg.production('bkpt_callfunc1 : ID ')
        def expression_callfunc(p):
            self.st.lookupFunction(p[0].value)
            ## todo era counter parms, local vars y temps
            self.reloadQuad.pushFilaPrincipal(["ERA", p[0].value], self.tempTable, self.constantTable, self.st, self.currentScope)
            self.callingFunc = p[0].value
            return p

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
        @self.pg.production('ciclo : for_loop')
        def expression_ciclo(p):
            return p

        @self.pg.production('for_loop : FOR LPARENS  expresion_comp PTOCOM asign_op RPARENS bloque')
        def expression_forloop(p):
            return p

        @self.pg.production('wh_loop : WHILE bktCondWhile cond_body bktAfterCondW bktWhile bloque')
        def expression_whloop(p):
            self.reloadQuad.finWhile()
            # self.reloadQuad.updateJumpPendiente()
            # self.reloadQuad.pushFilaPrincipal(["Goto", ""])
            return p
    
        @self.pg.production('bktCondWhile : ')
        def expression_bktcondwhile(p):
            self.reloadQuad.pushJumpFirstWhile()

        @self.pg.production('bktWhile : ')
        def expression_bktwhile(p):
            self.reloadQuad.pushFilaPrincipal(["GotoF", "", "t" + str(self.currGlobal)], self.tempTable, self.constantTable, self.st, self.currentScope)
    
        @self.pg.production('bktAfterCondW : ')
        def expresspktfinwhile(p):
            self.reloadQuad.pushJumpFirstWhile()
            return "owo"

        @self.pg.production('declaracion : tipo ID EQ constante PTOCOM')
        @self.pg.production('declaracion : tipo ID EQ STRING PTOCOM')
        @self.pg.production('declaracion : tipo asign_op PTOCOM')
        def expression_declaracion_compleja(p):
            plana = self.ut.flatten(p)[3:]
            q, currTemp, quadType = self.qd.evaluateQuadruple(plana,self.st, self.currentScope,self.currGlobal)
            nuevaQ = copy.deepcopy(q)
            self.qd.clearQueue()
            self.currGlobal = currTemp
            nuevaQ.items = self.tempTable.transformTemps(nuevaQ.items, self.mem)
            self.reloadQuad.pushQuadArithmeticQueue(nuevaQ, self.tempTable, self.constantTable, self.st, self.currentScope)
            return p

        @self.pg.production('declaracion : tipo ID PTOCOM')
        @self.pg.production('declaracion : tipo ID arr_idx PTOCOM')
        def expression_declaracion(p): 
            return p

        @self.pg.production('asignacion : ID EQ ID PTOCOM')
        @self.pg.production('asignacion : ID EQ STRING PTOCOM')
        def expresion_asignacion_arithm(p):
            var1Val = self.st.lookupVar(p[0].value, self.currentScope)
            var1Type = self.st.lookupType(p[0].value, self.currentScope)
            if(p[2].gettokentype() == "STRING"):
                self.reloadQuad.pushFilaPrincipal(["=", p[2].value, p[0].value], self.tempTable, self.constantTable, self.st, self.currentScope)
            else:
                var2Val = self.st.lookupVar(p[2].value, self.currentScope)
                var2Type = self.st.lookupType(p[2].value, self.currentScope)
                
                tipoOp = self.sCube.validateType(var1Type, var2Type)
                if tipoOp != 'ERR':
                    self.reloadQuad.pushFilaPrincipal(["=", p[2].value, p[0].value], self.tempTable, self.constantTable, self.st, self.currentScope)               
            return p
            
        @self.pg.production('asignacion : asign_op PTOCOM')
        def expresion_asignacionog(p):
            plana = self.ut.flatten(p)
            if(len(plana) == 4):
                var1Val = plana[0].value
                var1Type = self.st.lookupType(plana[0].value, self.currentScope)
                if (isinstance(plana[2], float) or isinstance(plana[2], int) or  isinstance(plana[2], bool) or  isinstance(plana[2], str)):
                    var2Val = plana[2]
                    var2Type = type(plana[2])
                else:
                    var2Val = plana[2].value
                    var2Type = self.st.lookupType(plana[2].value, self.currentScope)
                self.reloadQuad.pushFilaPrincipal(["=", var2Val, var1Val], self.tempTable, self.constantTable, self.st, self.currentScope)
            else:            
                q, currTemp, quadType = self.qd.evaluateQuadruple(plana[2:], self.st, self.currentScope,self.currGlobal)
                var1Type = self.st.lookupType(plana[0].value, self.currentScope)
                var2Val = q.top()[3]
                tipoOp = self.sCube.validateType(var1Type, quadType)
                self.currGlobal = currTemp
                if tipoOp != 'ERR':
                    nuevaQ = copy.deepcopy(q)
                    self.qd.clearQueue()
                    nuevaQ.items = self.tempTable.transformTemps(nuevaQ.items,  self.mem)
                    self.currGlobal = currTemp
                    self.reloadQuad.pushQuadArithmeticQueue(nuevaQ, self.tempTable, self.constantTable, self.st, self.currentScope)
                    print("pushed arithm", plana)
                    arg = nuevaQ.tail()[3]
                    self.reloadQuad.pushFilaPrincipal(["=", arg, self.ut.getValue(plana[2])], self.tempTable, self.constantTable, self.st, self.currentScope)
            return p

        @self.pg.production('asignacion : ID EQ call_func PTOCOM')
        def expression_asignacion(p):
            plana = self.ut.flatten(p)
            
            return p

        @self.pg.production('asignacion : ID arr_idx EQ expresion PTOCOM')
        def expression_asignacionarrays(p):
            return p

        @self.pg.production('asign_op : ID EQ expresion')
        def expresion_asignacion(p):
            return p

        @self.pg.production('arr_idx : CORCH_LEFT CTE_ENT CORCH_RIGHT')
        def expression_arridx(p):
            return p

        @self.pg.production('escritura : PRINT LPARENS esc_aux_helper RPARENS PTOCOM')
        def expression_escritura(p):
            self.ut.handlePrintStatements(self.tempWrite, self.st, self.currentScope, self.currGlobal, self.reloadQuad, self.qd, self.tempTable, self.mem, self.constantTable)
            self.tempWrite = []
            return p

        @self.pg.production('esc_aux_helper : escaux esc_aux_helper')
        @self.pg.production('esc_aux_helper : escaux')
        def expression_progauxfunc(p):
            plana = self.ut.flatten(p[0])
            self.tempWrite.insert(0, plana)
            return p

        @self.pg.production('escaux : expresion COMM')
        @self.pg.production('escaux : expresion')
        @self.pg.production('escaux : STRING COMM')
        @self.pg.production('escaux : STRING')
        def print_strings(p):
            return p[0]

        @self.pg.production('expresion : expresion_comp')
        @self.pg.production('expresion : exp')
        def expression_expresion(p):
            return p
        
        @self.pg.production('expresion_comp : exp EQUALITY exp')
        @self.pg.production('expresion_comp : exp MOTHN exp')
        @self.pg.production('expresion_comp : exp LETHN exp')
        @self.pg.production('expresion_comp : exp NEQ exp')
        def expression_expcomp(p):
            primeraParte = self.ut.flatten(p[0])
            segundaParte = self.ut.flatten(p[2])
            val,valType, val2 , val2Type = [0 for _ in range(4)]

            if(len(primeraParte) > 1):
                q1, currTemp, valType = self.qd.evaluateQuadruple(primeraParte,self.st, self.currentScope,self.currGlobal)
                nuevaQ1 = copy.deepcopy(q1)
                nuevaQ1.items = self.tempTable.transformTemps(nuevaQ1.items,  self.mem)
                self.currGlobal = currTemp
                self.qd.clearQueue()
                self.reloadQuad.pushQuadArithmeticQueue(nuevaQ1, self.tempTable, self.constantTable, self.st, self.currentScope)
                val = nuevaQ1.top()[3]
            else:
                val = primeraParte[0]
                valType = self.ut.convertTypes(primeraParte[0])
                if(valType == 'ID'):
                    valType = self.st.lookupType(val.value, self.currentScope)

            if(len(segundaParte) > 1):
                q2, currTemp, val2Type = self.qd.evaluateQuadruple(segundaParte,self.st, self.currentScope,self.currGlobal)
                nuevaQ2 = copy.deepcopy(q2)
                self.qd.clearQueue()
                nuevaQ2.items = self.tempTable.transformTemps(nuevaQ2.items, self.mem)
                self.reloadQuad.pushQuadArithmeticQueue(nuevaQ2, self.tempTable, self.constantTable, self.st, self.currentScope)
                val2 = nuevaQ2.top()[3]
                self.currGlobal = currTemp
            else:
                val2 = segundaParte[0]
                val2Type = self.ut.convertTypes(segundaParte[0])
                if(valType == 'ID'):
                    val2Type = self.st.lookupType(val.value, self.currentScope)

            isBool = self.sCube.validateOperationBool(valType, val2Type)
            self.currGlobal += 1
            if(isBool):
                res = "t" + str(self.currGlobal)
                self.tempTable.addSingleVar(res, self.mem)
                self.reloadQuad.pushFilaPrincipal([p[1].value, self.ut.getValue(val), self.ut.getValue(val2), "t" + str(self.currGlobal)], self.tempTable, self.constantTable, self.st, self.currentScope)
            else:
                raise Exception("!!", val, "cannot be compared to", val2, "!!")
            return "t" + str(self.currGlobal)   
                    
        @self.pg.production('condicion : IF cond_body gotof bloque cond_aux fincond')
        def expression_condicion(p):
            return p

        @self.pg.production('fincond : ')
        def bkpoint_gotof(p):
            self.reloadQuad.updateJumpPendiente()

        @self.pg.production('gotof : ')
        def bkpoint_gotof(p):
            self.reloadQuad.pushFilaPrincipal(["GotoF", "", "t" + str(self.currGlobal)], self.tempTable, self.constantTable, self.st, self.currentScope)
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

        @self.pg.production('constante : ID') 
        @self.pg.production('constante : VERDADERO')
        @self.pg.production('constante : FALSO')
        @self.pg.production('constante : numero')
        @self.pg.production('constante : STRING') 
        def expression_constante(p):
            return p

        @self.pg.production('numero : CTE_FLOAT')
        @self.pg.production('numero : CTE_ENT')
        def expresion_numero(p):
            if p[0].gettokentype() == 'CTE_FLOAT':
                self.constantTable.add(float(p[0].value), self.mem)
                return float(p[0].value)
            elif p[0].gettokentype() == 'CTE_ENT':
                self.constantTable.add(int(p[0].value), self.mem)
                return int(p[0].value)

        @self.pg.production('left_paren : LPARENS')
        def expresion_parens(p):
            return p[0].value

        @self.pg.production('test_grammar : RPARENS PTOCOM')
        def test_grammar(p):
            return p

        @self.pg.error
        def error_handler(token):
            raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype(), token)

    def get_parser(self):
        return self.pg.build()