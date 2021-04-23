from rply import ParserGenerator
from ast import Termino

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['PROGRAMA', 'IF', 'ELSE', 'VAR', 'PRINT', 'WHILE', 'INT', 'STR', 'FLOT', 'LPARENS', 'RPARENS', 'LKEY', 'RKEY', 'SUM', 'SUB',
            'MUL', 'DIV', 'EQ', 'COLN', 'COMM', 'PTO', 'PTOCOM', 'MOTHN', 'LETHN', 'NEQ', 'CORCH_LEFT', 'CORCH_RIGHT', 'CORCH_LEFT',
            'FOR', 'FUNCION', 'VACIO'
            ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV'])
            ]
        )

    def parse(self):
        @self.pg.production('programa : PROGRAMA ID COLN prog_aux')
        @self.pg.production('programa : PROGRAMA ID COLN prog_aux prog_aux_func ')
        def expression_parens(p):
            return Termino()

        @self.pg.production('prog_aux : vars bloque')
        @self.pg.production('prog_aux : bloque')
        def expression_parens(p):
            return Termino()
		

        @self.pg.production('prog_aux_func : func prog_aux_func')
        @self.pg.production('prog_aux_func : func')
        def expression_parens(p):
            return Termino()

        @self.pg.production('vars : VAR varaux COLN tipo PTOCOM')
        def expression_parens(p):
            return Termino()

        @self.pg.production('varaux : ID COMM varaux')
        @self.pg.production('varaux : ID')
        def expression_parens(p):
            return Termino()

        @self.pg.production('tipo : INT')
        @self.pg.production('tipo : FLOT')
        @self.pg.production('tipo : STR')
        def expression_parens(p):
            return Termino()

        @self.pg.production('tipo_funcs : tipo')
        @self.pg.production('tipo_funcs : VACIO')
        def expression_parens(p):
            return Termino()

        @self.pg.production('bloque : LKEY bloqaux RKEY')
        def expression_parens(p):
            return Termino()

        @self.pg.production('bloqaux : estatuto bloqaux')
        @self.pg.production('bloqaux : estatuto')
        def expression_parens(p):
            return Termino()

        @self.pg.production('func : tipo_funcs FUNCION ID LPARENS parms RPARENS bloque')
        def expression_parens(p):
            return Termino()

        @self.pg.production('parms : tipo ID COMM parms')
        @self.pg.production('parms : tipo ID')
        def expression_parens(p):
            return Termino()

        @self.pg.production('estatuto : call_func')
        @self.pg.production('estatuto : declaracion')
        @self.pg.production('estatuto : asignacion')
        @self.pg.production('estatuto : condicion')
        @self.pg.production('estatuto : escritura')
        @self.pg.production('estatuto : ciclo')
        def expression_parens(p):
            return Termino()

        @self.pg.production('call_func : ID LPARENS call_func_aux RPARENS PTOCOM')
        def expression_parens(p):
            return Termino()

        @self.pg.production('call_func_aux : accepted_params COMM call_func_aux')
        @self.pg.production('call_func_aux : accepted_params')
        def expression_parens(p):
            return Termino()

        @self.pg.production('accepted_params : constante')
        @self.pg.production('accepted_params : STRING')
        def expression_parens(p):
            return Termino()

        @self.pg.production('ciclo : wh_loop')
        @self.pg.production('ciclo : wh_loop')
        def expression_parens(p):
            return Termino()

        @self.pg.production('for_loop : FOR LPARENS INT ID EQ exp PTOCOM expresion_comp PTOCOM asign_op RPARENS bloque')
        def expression_parens(p):
            return Termino()

        @self.pg.production('wh_loop : WHILE cond_body bloque')
        def expression_parens(p):
            return Termino()

        @self.pg.production('declaracion : tipo ID PTOCOM')
        @self.pg.production('declaracion : tipo ID arr_idx PTOCOM')
        def expression_parens(p):
            return Termino()

        @self.pg.production('asignacion : asign_op PTOCOM')
        @self.pg.production('asignacion : ID arr_idx EQ expresion PTOCOM')
        @self.pg.production('asignacion : ID EQ STRING PTOCOM')
        def expression_parens(p):
            return Termino()
        
        @self.pg.production('asignacion : ID EQ STRING PTOCOM')
        def expression_parens(p):
            return Termino()

        @self.pg.production('asign_op : PRINT OPEN_PARENS escrHelperA CLOSE_PARENS SEMICOLON')
        def expression_parens(p):
            return Termino()

        @self.pg.production('arr_idx : CORCH_LEFT CONSTANTE_ENT CORCH_RIGHT')
        def expression_parens(p):
            return Termino()

        @self.pg.production('escritura : PRINT LPARENS escaux RPARENS PTOCOM')
        def expression_parens(p):
            return Termino()

        @self.pg.production('escaux : expresion COMM escaux')
        @self.pg.production('escaux : STRING COMM escaux')
        @self.pg.production('escaux : expresion')
        @self.pg.production('escaux : STRING')
        def expression_parens(p):
            return Termino()

        @self.pg.production('expresion : expresion_comp')
        @self.pg.production('expresion : exp')
        def expression_parens(p):
            return Termino()
    
        @self.pg.production('expresion_comp : exp MOTHN exp')
        @self.pg.production('expresion_comp : exp LETHN exp')
        @self.pg.production('expresion_comp : exp NEQ exp')
        def expression_parens(p):
            return Termino()

        @self.pg.production('condicion : IF cond_body bloque cond_aux')
        def expression_parens(p):
            return Termino()

        @self.pg.production('cond_body : LPARENS expresion RPARENS')
        def expression_parens(p):
            return Termino()

        @self.pg.production('cond_aux : ELSE bloque PTOCOM')
        @self.pg.production('cond_aux : PTOCOM')
        def expression_parens(p):
            return Termino()

        @self.pg.production('exp : termino SUM exp')
        @self.pg.production('exp : termino SUB exp')
        @self.pg.production('exp : termino')
        def expression_parens(p):
            return Termino()

        @self.pg.production('termino : factor MUL termino')
        @self.pg.production('termino : factor DIV termino')
        @self.pg.production('termino : factor')
        def expression_parens(p):
            return Termino()

        @self.pg.production('factor : OPEN_PARENS expresion CLOSE_PARENS')
        @self.pg.production('factor : SUM var_cte')
        @self.pg.production('factor : SUB var_cte')
        @self.pg.production('factor : var_cte')
        def expression_parens(p):
            return Termino()

        @self.pg.production('constante : ID')
        @self.pg.production('constante : CTE_FLOAT')
        @self.pg.production('constante : CTE_INT')
        def expression_number(p):
            return Termino()

    def get_parser(self):
        return self.pg.build()