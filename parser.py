from rply import ParserGenerator
from ast import Termino

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['OPEN_PARENS', 'CLOSE_PARENS',
            'PLUS', 'MINUS', 'MUL', 'DIV', 'IF', 'ID', 'PROGRAM', 'COLON', 'LEFTOP', 'RIGHTOP',
            'EQUALS', 'SEMICOLON', 'STRING', 'PRINT', 'OPEN_CURLY', 'CLOSE_CURLY', 'ELSE', 'VAR', 'COMMA', 'INT',
            'FLOAT', 'CTE_INT', 'CTE_FLOAT', 'NOTEQ'
            ],
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=[
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MUL', 'DIV'])
            ]
        )

    def parse(self):
        @self.pg.production('programa : PROGRAM ID SEMICOLON programAux bloque')
        def expression_parens(p):
            return Termino()

        @self.pg.production('programAux : vars')
        @self.pg.production('programAux : estatuto')
        def expression_parens(p):
            return Termino()

        @self.pg.production('vars : VAR varsAuxA COLON tipo SEMICOLON')
        def expression_parens(p):
            return Termino()

        @self.pg.production('varsAuxA : ID COMMA varsAuxA')
        @self.pg.production('varsAuxA : ID')
        def expression_parens(p):
            return Termino()

        @self.pg.production('bloque : OPEN_CURLY estatuto CLOSE_CURLY')
        def expression_parens(p):
            return Termino()

        @self.pg.production('estatuto : condicion estatuto')
        @self.pg.production('estatuto : asignacion estatuto')
        @self.pg.production('estatuto : escritura estatuto')
        @self.pg.production('estatuto : escritura')
        @self.pg.production('estatuto : asignacion')
        @self.pg.production('estatuto : condicion')
        def expression_parens(p):
            return Termino()

        @self.pg.production('condicion : IF OPEN_PARENS expresion CLOSE_PARENS bloque SEMICOLON')
        @self.pg.production('condicion : IF OPEN_PARENS expresion CLOSE_PARENS bloque ELSE bloque SEMICOLON')
        def expression_parens(p):
            return Termino()

        @self.pg.production('escritura : PRINT OPEN_PARENS escrHelperA CLOSE_PARENS SEMICOLON')
        def expression_parens(p):
            return Termino()

        @self.pg.production('escrHelperA : expresion COMMA escrHelperA')
        @self.pg.production('escrHelperA : STRING COMMA escrHelperA')
        @self.pg.production('escrHelperA : STRING')
        @self.pg.production('escrHelperA : expresion')
        def expression_parens(p):
            return Termino()

        @self.pg.production('asignacion : ID EQUALS expresion SEMICOLON')
        def expression_parens(p):
            return Termino()

        @self.pg.production('expresion : exp NOTEQ exp')
        @self.pg.production('expresion : exp LEFTOP exp')
        @self.pg.production('expresion : exp RIGHTOP exp')
        @self.pg.production('expresion : exp')
        def expression_parens(p):
            return Termino()

        @self.pg.production('exp : termino PLUS exp')
        @self.pg.production('exp : termino MINUS exp')
        @self.pg.production('exp : termino')
        def expression_parens(p):
            return Termino()

        @self.pg.production('termino : factor MUL termino')
        @self.pg.production('termino : factor DIV termino')
        @self.pg.production('termino : factor')
        def expression_parens(p):
            return Termino()

        @self.pg.production('factor : OPEN_PARENS expresion CLOSE_PARENS')
        @self.pg.production('factor : PLUS var_cte')
        @self.pg.production('factor : MINUS var_cte')
        @self.pg.production('factor : var_cte')
        def expression_parens(p):
            return Termino()

        @self.pg.production('tipo : INT')
        @self.pg.production('tipo : FLOAT')
        def expression_number(p):
            return Termino()

        @self.pg.production('var_cte : ID')
        @self.pg.production('var_cte : CTE_FLOAT')
        @self.pg.production('var_cte : CTE_INT')
        def expression_number(p):
            return Termino()

    def get_parser(self):
        return self.pg.build()