import rply
from rply import ParserGenerator
from Utils.ast import Termino, Declaracion, Tipo
from Utils.symbolTable import SymbolTable
from Utils.semantic import SemanticCube
from Utils.UtilFuncs import UtilFuncs
import pprint
pp = pprint.PrettyPrinter(indent=4)

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['PROGRAMA', 'IF', 'ELSE', 'PRINT', 'WHILE', 'INT', 'STR', 'FLOT', 'LPARENS', 'RPARENS', 'LKEY', 'RKEY', 'SUM', 'SUB',
            'MUL', 'DIV', 'EQ', 'COMM', 'PTOCOM', 'MOTHN', 'LETHN', 'NEQ', 'CORCH_LEFT', 'CORCH_RIGHT', 'CORCH_LEFT',
            'FOR', 'FUNCION', 'VACIO', 'ID', 'STRING', 'LPARENS', 'RPARENS', 'CTE_ENT', 'CTE_FLOAT', 'EXCL'
            ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV'])
            ]
        )
        self.st = SymbolTable()
        self.ut = UtilFuncs()
        self.isMain = 1
        self.currentScope= "main"
        self.sCube = SemanticCube()
        self.hasStarted = 0

    def parse(self):

        @self.pg.production('empezando : programa')
        @self.pg.production('empezando : func_declarOG programa')
        def expression_empezando(p):
            return p

        @self.pg.production('programa : PROGRAMA ID func_bloque')
        @self.pg.production('programa : PROGRAMA ID func_bloque prog_aux_func')
        def expression_programa(p):
            self.st.printSymbolTable()
            return p

        @self.pg.production('prog_aux_func : func prog_aux_func')
        @self.pg.production('prog_aux_func : func')
        def expression_progauxfunc(p):
            return p

        @self.pg.production('tipo : INT')
        @self.pg.production('tipo : FLOT')
        @self.pg.production('tipo : STR')
        def expression_tipo(p):
            return p[0]

        @self.pg.production('tipo_funcs : tipo')
        @self.pg.production('tipo_funcs : VACIO')
        def expression_tipo_func(p):
            return p[0]

        @self.pg.production('func_bloque : LKEY bloqaux RKEY PTOCOM')
        def expression_fun_bloque(p):
            print("Curr bloque !")
            # print(self.ut.getLatestFuncNameQ())
            self.currentScope = self.ut.getLatestFuncNameQ()
            print(self.currentScope)
            # self.currentScope = "1" + p[2].value
            if(self.isMain):
                self.st.closeCurrScope(p, "main", "null")
                self.isMain = 0
            return p[1]

        @self.pg.production('bloque : LKEY bloqaux RKEY')
        def expression_bloque(p):
            return p[1]

        @self.pg.production('bloqaux : estatuto bloqaux')
        @self.pg.production('bloqaux : estatuto')
        def expression_bloqaux(p):
            return p

        @self.pg.production('func_declarOG : tipo_funcs FUNCION ID LPARENS parms RPARENS EXCL func_declarOG')
        @self.pg.production('func_declarOG : tipo_funcs FUNCION ID LPARENS parms RPARENS EXCL')
        def expression_parms(p):
            self.st.processFuncDeclP(p)
            self.ut.addFunctionNameQ(p[2].value)
            return p

        @self.pg.production('func : tipo_funcs FUNCION ID LPARENS parms RPARENS func_bloque')
        def expression_func(p):
            if(self.isMain == 0):
                self.st.closeCurrScope(p[6], p[2].value, p[0].value)
            return p

        @self.pg.production('parms : tipo ID COMM parms')
        @self.pg.production('parms : tipo ID')
        def expression_parms(p):
            return p

        @self.pg.production('estatuto : call_func')
        @self.pg.production('estatuto : declaracion')
        @self.pg.production('estatuto : asignacion')
        @self.pg.production('estatuto : condicion')
        @self.pg.production('estatuto : escritura')
        @self.pg.production('estatuto : ciclo')
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
            return p

        @self.pg.production('declaracion : tipo ID PTOCOM')
        @self.pg.production('declaracion : tipo ID arr_idx PTOCOM')
        def expression_declaracion(p):
            print("Declaring!" , p)
            if(self.isMain == 1):
                self.st.addVarMainScope(p)
            else:
                self.st.addVarNormalScope(p, self.currentScope)
            return p

        @self.pg.production('asignacion : asign_op PTOCOM')
        @self.pg.production('asignacion : ID arr_idx EQ expresion PTOCOM')
        @self.pg.production('asignacion : ID EQ STRING PTOCOM')
        def expression_asignacion(p):
            plana = self.st.flatten(p)
            leftType = self.st.lookupType(plana[0].value, self.currentScope)
            if(self.sCube.validateType(leftType, plana[2].gettokentype())):
                self.st.addValue(plana[0].value, plana[2].value, self.currentScope)
            return p
        
        @self.pg.production('asign_op : ID EQ expresion')
        def expression_asignop(p):
            return p

        @self.pg.production('arr_idx : CORCH_LEFT CTE_ENT CORCH_RIGHT')
        def expression_arridx(p):
            return p

        @self.pg.production('escritura : PRINT LPARENS escaux RPARENS PTOCOM')
        def expression_escritura(p):
            return p

        @self.pg.production('escaux : expresion COMM escaux')
        @self.pg.production('escaux : STRING COMM escaux')
        @self.pg.production('escaux : expresion')
        @self.pg.production('escaux : STRING')
        def expression_escaux(p):
            return p

        @self.pg.production('expresion : expresion_comp')
        @self.pg.production('expresion : exp')
        def expression_expresion(p):
            return p
    
        @self.pg.production('expresion_comp : exp MOTHN exp')
        @self.pg.production('expresion_comp : exp LETHN exp')
        @self.pg.production('expresion_comp : exp NEQ exp')
        def expression_expcomp(p):
            return p

        @self.pg.production('condicion : IF cond_body bloque cond_aux')
        def expression_condicion(p):
            return p

        @self.pg.production('cond_body : LPARENS expresion RPARENS')
        def expression_condBody(p):
            return p

        @self.pg.production('cond_aux : ELSE bloque PTOCOM')
        @self.pg.production('cond_aux : PTOCOM')
        def expression_condAux(p):
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

        @self.pg.production('factor : LPARENS expresion RPARENS')
        @self.pg.production('factor : SUM constante')
        @self.pg.production('factor : SUB constante')
        @self.pg.production('factor : constante')
        def expression_factor(p):
            return p

        @self.pg.production('constante : ID')
        @self.pg.production('constante : CTE_FLOAT')
        @self.pg.production('constante : CTE_ENT')
        def expression_constante(p):
            return p

        @self.pg.error
        def error_handler(token):
            raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())

    def get_parser(self):
        return self.pg.build()