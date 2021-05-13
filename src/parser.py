import rply
from rply import ParserGenerator
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs
from Utils.quadruples import Quadruple
from Utils.Stack import Stack
from Utils.Queue import Queue
from Utils.QuadReloaded import QuadReloaded
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
            'CTE_FLOAT', 'EXCL','BOOLEANO', 'EQUALITY', 'VERDADERO', 'FALSO', 'PRINCIPAL', 
            'VAR', 'COLON'
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
        self.isMain = 1
        self.currentScope= "global"
        self.sCube = SemanticCube()
        self.hasStarted = 0
        self.isInTempScope = False
        self.tempNum = 0
        self.prevScope = ""
        self.addingCurrType = "null"
        self.currGlobal = 0
        

    def parse(self):
        @self.pg.production('empezando : programa')
        def expression_empezando(p):
            return p

        @self.pg.production('programa : PROGRAMA ID PTOCOM many_vars func principal_driver')
        @self.pg.production('programa : PROGRAMA ID PTOCOM many_vars principal_driver')
        def expression_programa(p):
            # print("programagrammar",p)
            self.st.printSt()
            self.reloadQuad.printFilaPrincipal()
            return p

        @self.pg.production('prog_aux_func : func prog_aux_func')
        @self.pg.production('prog_aux_func : func')
        def expression_progauxfunc(p):
            return p

        @self.pg.production('principal_driver : PRINCIPAL LPARENS RPARENS func_bloque')
        def expression_progauxfunc(p):
            return p
        
        @self.pg.production('many_vars : vars many_vars')
        @self.pg.production('many_vars : vars')
        def expression_progauxfunc(p):
            return p

        # @self.pg.production('declarar_main : declare_vars PTOCOM')
        @self.pg.production('vars : VAR varsAuxA COLON tipo PTOCOM')
        def expression_addingvar(p):
            self.st.processVars(p[1], p[3], self.currentScope)
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

        @self.pg.production('tipo_funcs : tipo')
        @self.pg.production('tipo_funcs : VACIO')
        def expression_tipo_func(p):
            # print("TIPOFUNCC")
            return p[0]

        @self.pg.production('func_bloque : LKEY bloqaux RKEY PTOCOM')
        def expression_fun_bloque(p):
            # self.currentScope = self.ut.getLatestFuncNameQ()
            # if(self.isMain):
            #     self.st.closeCurrScope("main", "null")
            #     self.isMain = 0
            return p[1]

        @self.pg.production('bloque : LKEY bloqaux RKEY')
        def expression_bloque(p):
            # if(self.isInTempScope):
            return p[1]

        @self.pg.production('bloqaux : estatuto bloqaux')
        @self.pg.production('bloqaux : estatuto')
        def expression_bloqaux(p):
            return p

        @self.pg.production('func_aux : func_declarOG func_aux')
        @self.pg.production('func_aux : func_declarOG')
        def expression_bloqaux(p):
            return p

        @self.pg.production('func_declarOG : tipo_funcs FUNCION ID LPARENS RPARENS EXCL')
        def expression_funcdeclarOG_Empty(p):
        #     self.st.declareFuncInSymbolTable(p)
        #     self.ut.addFunctionNameQ(p[2].value)
            return p


        @self.pg.production('func_declarOG : tipo_funcs FUNCION ID LPARENS parms RPARENS EXCL')
        def expression_funcdeclarOG(p):
            # self.st.processFuncDeclP(p)
            # self.ut.addFunctionNameQ(p[2].value)
            return p

        @self.pg.production('func : FUNCION tipo_funcs ID LPARENS RPARENS func_bloque')
        def expression_func(p):
            # print("ENTRANDO A FUNC")
            # if(self.isMain == 0):
            #     self.st.closeCurrScope(p[2].value, p[0].value)
            return p

        @self.pg.production('parms : tipo ID COMM parms')
        @self.pg.production('parms : tipo ID')
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
            return p

        @self.pg.production('call_func : ID LPARENS call_func_aux RPARENS PTOCOM')
        def expression_callfunc(p):
            return p

        @self.pg.production('call_func_aux : accepted_params COMM call_func_aux')
        @self.pg.production('call_func_aux : accepted_params')
        def expression_callfuncaux(p):
            return p

        @self.pg.production('accepted_params : constante')
        @self.pg.production('accepted_params : STRING')
        @self.pg.production('accepted_params : call_func')
        def expression_acceptedparams(p):
            return p

        @self.pg.production('ciclo : wh_loop')
        @self.pg.production('ciclo : for_loop')
        def expression_ciclo(p):
            return p

        @self.pg.production('for_loop : FOR LPARENS INT ID EQ exp PTOCOM expresion_comp PTOCOM asign_op RPARENS bloque')
        def expression_forloop(p):
            return p

        @self.pg.production('wh_loop : WHILE cond_body bloque')
        def expression_whloop(p):
            # print("WHILE", p[1])                
            return p

        @self.pg.production('declaracion : tipo ID EQ constante PTOCOM')
        @self.pg.production('declaracion : tipo ID EQ STRING PTOCOM')
        @self.pg.production('declaracion : tipo asign_op PTOCOM')
        def expression_declaracion_compleja(p):
            plana = self.ut.flatten(p)[3:]
            q, currTemp, quadType = self.qd.evaluateQuadruple(plana,self.st, self.currentScope,0)
            nuevaQ = copy.deepcopy(q)
            self.qd.clearQueue()
            self.currGlobal = currTemp
            self.reloadQuad.pushQuadArithmeticQueue(nuevaQ)
            # for q_item in q.queue:
            #     print("QUADBOY", q_item)
            # self.st.addVarNormalScope(p, self.currentScope, ans)
            return p

        @self.pg.production('declaracion : tipo ID PTOCOM')
        @self.pg.production('declaracion : tipo ID arr_idx PTOCOM')
        def expression_declaracion(p):
            # plana = self.ut.flatten(p)
            # if(len(p) == 3):
            #     self.st.addVarNormalScope(p, self.currentScope, "")
            # else:
            #     sz = int(plana[3].value)
            #     initArr = self.st.populateEmptyArray(sz)
            #     self.st.addArraynotInit(plana, self.currentScope, initArr)
            return p

        @self.pg.production('asignacion : ID EQ ID PTOCOM')
        @self.pg.production('asignacion : ID EQ STRING PTOCOM')
        def expresion_asignacion_arithm(p):
            var1Val = self.st.lookupVar(p[0].value, self.currentScope)
            var1Type = self.st.lookupType(p[0].value, self.currentScope)
            if(p[2].gettokentype() == "STRING"):
                self.reloadQuad.pushFilaPrincipal(["=", p[0].value, p[2].value])
            else:
                var2Val = self.st.lookupVar(p[2].value, self.currentScope)
                var2Type = self.st.lookupType(p[2].value, self.currentScope)
                
                tipoOp = self.sCube.validateType(var1Type, var2Type)
                if tipoOp != 'ERR':
                    self.reloadQuad.pushFilaPrincipal(["=", p[0].value, p[1].value])               
            return p
            
        @self.pg.production('asignacion : asign_op PTOCOM')
        def expresion_asignacion_arithm(p):
            plana = self.ut.flatten(p)
            if(len(plana) == 4):
                var1Val = plana[0].value
                var1Type = self.st.lookupType(plana[0].value, self.currentScope)
                if(isinstance(plana[2], float) or  isinstance(plana[2], int) or  isinstance(plana[2], bool) or  isinstance(plana[2], str)):
                    var2Val = plana[2]
                    var2Type = type(plana[2])
                else:
                    var2Val = plana[2].value
                    var2Type = self.st.lookupType(plana[2].value, self.currentScope)
                
                self.reloadQuad.pushFilaPrincipal(["=", plana[0], plana[2]])
            else:            
                q, currTemp, quadType = self.qd.evaluateQuadruple(plana[2:], self.st, self.currentScope,0)
                var1Type = self.st.lookupType(plana[0].value, self.currentScope)
                var2Val = q.top()[3]
                tipoOp = self.sCube.validateType(var1Type, quadType)
                if tipoOp != 'ERR':
                    nuevaQ = copy.deepcopy(q)
                    self.qd.clearQueue()
                    self.currGlobal = currTemp
                    self.reloadQuad.pushQuadArithmeticQueue(nuevaQ)
                    self.reloadQuad.pushFilaPrincipal(["=", plana[0].value, var2Val])
            return p

        @self.pg.production('asignacion : ID EQ call_func PTOCOM')
        def expression_asignacion(p):
            plana = self.ut.flatten(p)
            # leftType = self.st.lookupType(plana[0].value, self.currentScope)
            # # TODO
            # # checar que los vals puedan ser mandados a operacion y si no
            # # mandarlos a los cuadruplos
            # if(self.sCube.validateType(leftType, self.ut.convertTypes(plana[2])) != 'ERR'):
            #     self.st.addValue(plana[0].value, plana[2].value, self.currentScope)
            return p

        @self.pg.production('asignacion : ID arr_idx EQ expresion PTOCOM')
        def expression_asignacionarrays(p):
            # plana = self.ut.flatten(p)
            # leftType = self.st.lookupType(plana[0].value, self.currentScope)
            # # TODO
            # # checar que los vals puedan ser mandados a operacion y si no
            # # mandarlos a los cuadruplos
            # if(self.sCube.validateType(leftType, self.ut.convertTypes(plana[2])) != 'ERR'):
            #     self.st.addValue(plana[0].value, plana[2].value, self.currentScope)
            return p

        @self.pg.production('asign_op : ID EQ expresion')
        def expression_asignop(p):
            return p

        @self.pg.production('arr_idx : CORCH_LEFT CTE_ENT CORCH_RIGHT')
        def expression_arridx(p):
            return p

        @self.pg.production('escritura : PRINT LPARENS esc_aux_helper RPARENS PTOCOM')
        def expression_escritura(p):
            printedIt = self.ut.flatten(p[2])
            self.reloadQuad.parsePrint(printedIt)
            # self.reloadQuad.printFilaPrincipal()
            return p

        @self.pg.production('esc_aux_helper : escaux esc_aux_helper')
        @self.pg.production('esc_aux_helper : escaux')
        def expression_progauxfunc(p):
            return p

        @self.pg.production('escaux : STRING COMM')
        @self.pg.production('escaux : STRING')
        def print_strings(p):
            print("just escaux things ",p)
            return p[0]


        @self.pg.production('escaux : expresion COMM')
        @self.pg.production('escaux : expresion')
        def expression_escaux(p):
            planaOp = self.ut.flatten(p[0])
            q, currTemp, quadType = self.qd.evaluateQuadruple(planaOp, self.st, self.currentScope, self.currGlobal)
            nuevaQ = copy.deepcopy(q)
            self.qd.clearQueue()
            self.currGlobal = currTemp
            self.reloadQuad.pushQuadArithmeticQueue(nuevaQ)
            return "t" + str(currTemp)

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
            print(primeraParte)
            print(segundaParte)
            val,valType, val2 , val2Type = [0 for _ in range(4)]
            # grade_1, grade_2, grade_3, average = [0.0 for _ in range(4)]

            print("types", valType, val2Type)
            if(len(primeraParte) > 1):
                q1, currTemp, valType = self.qd.evaluateQuadruple(primeraParte,self.st, self.currentScope,0)
                nuevaQ1 = copy.deepcopy(q1)
                self.qd.clearQueue()
                self.reloadQuad.pushQuadArithmeticQueue(nuevaQ1)
                val = nuevaQ1.top()[3]
            else:
                val = primeraParte[0]
                valType = self.ut.convertTypes(primeraParte[0])

            if(len(segundaParte) > 1):
                q2, currTemp, val2Type = self.qd.evaluateQuadruple(segundaParte,self.st, self.currentScope,0)
                nuevaQ2 = copy.deepcopy(q2)
                self.qd.clearQueue()
                self.reloadQuad.pushQuadArithmeticQueue(nuevaQ2)
                val2 = nuevaQ2.top()[3]
            else:
                val2 = segundaParte[0]
                val2Type = self.ut.convertTypes(segundaParte[0])

            isBool = self.sCube.validateOperationBool(valType, val2Type)
            if(isBool):
                self.reloadQuad.pushFilaPrincipal([p[1], val, val2, "t" + str(self.currGlobal)])
            else:
                raise Exception("!!", val, "cannot be compared to", val2, "!!")
            return p

        @self.pg.production('condicion : IF cond_body bloque cond_aux')
        def expression_condicion(p):
            
            # plana = self.ut.flatten(p)
            # self.st.printSt()
            # print("clear")
            # self.st.clearScope(self.currentScope)
            # self.st.printSt()
            # self.tempNum -=1
            # self.currentScope = self.prevScope
            # print("condbody eval", p[1])
            # print("patadas de ahogado")
            # print(test_grammar(p))
            return p

        @self.pg.production('cond_body : LPARENS expresion_comp RPARENS')
        def expression_condBody(p):
            # self.tempNum += 1
            # self.scopeStack.push(self.currentScope)
            # self.prevScope = self.currentScope
            # self.currentScope = "tempScope" + str(self.tempNum)
            # self.st.declareTempScope(self.tempNum, self.prevScope)
            return p[1] 

        @self.pg.production('cond_aux : ELSE bloque PTOCOM')
        @self.pg.production('cond_aux : PTOCOM')
        def expression_condAux(p):
            # plana = self.ut.flatten(p)
            # print("else",plana)
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
        def expression_constante(p):
            return p

        @self.pg.production('numero : CTE_FLOAT')
        @self.pg.production('numero : CTE_ENT')
        def expresion_numero(p):
            if p[0].gettokentype() == 'CTE_FLOAT':
                return float(p[0].value)
            elif p[0].gettokentype() == 'CTE_ENT':
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