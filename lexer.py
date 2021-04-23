from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        self.lexer.add('PROGRAMA', r'programa')
        self.lexer.add('IF', r'si')
        self.lexer.add('ELSE', r'\sino')
        self.lexer.add('VAR', r'var')
        self.lexer.add('PRINT', r'escribir')
        self.lexer.add('WHILE', r'mientras')
        self.lexer.add('INT', r'entero')
        self.lexer.add('TRU', r'verdadero')
        self.lexer.add('FAL', r'falso')
        self.lexer.add('STR', r'cadena')
        self.lexer.add('FLOT', r'flotante')
        self.lexer.add('COMMENT', r'\#')
        self.lexer.add('LPARENS', r'\(')
        self.lexer.add('RPARENS', r'\)')
        self.lexer.add('LKEY', r'\{')
        self.lexer.add('RKEY', r'\}')
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('EQ', r'\=')
        self.lexer.add('COLN', r'\:')
        self.lexer.add('COMM', r'\,')
        self.lexer.add('PTO', r'\.')
        self.lexer.add('PTOCOMM', r'\;')
	
		
        self.lexer.add("ID", r'[a-zA-Z_$][a-zA-Z_0-9]*')
        self.lexer.add('MOTHN', r'\>')
        self.lexer.add('LETHN', r'\<')
        self.lexer.add('NEQ', r'\<>')
        self.lexer.add('CORCH_LEFT', r'\[')
        self.lexer.add('CORCH_RIGHT', r'\]')
        self.lexer.add('FOR', r'\por')
        self.lexer.add('FUNCION', r'funcion')
        self.lexer.add('VACIO', r'vacio')

        self.lexer.add("STRING", r"\"([^\"\\]|\\.)*\"")
        self.lexer.add("CTE_FLOAT", r'(((0|[1-9][0-9]*)(\.[0-9]*)+)|(\.[0-9]+))([eE][\+\-]?[0-9]*)?')
        self.lexer.add('CTE_INT', r'\d+')
        self.lexer.ignore('\s+')


		

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()