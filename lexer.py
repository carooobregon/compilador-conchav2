from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        self.lexer.add("PRINT", r'print')
        self.lexer.add('INT', r'int')
        self.lexer.add('FLOAT', r'float')
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'/')
        self.lexer.add('OPEN_PARENS', r'\(')
        self.lexer.add('CLOSE_PARENS', r'\)')
        self.lexer.add('VAR', r'var')
        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('PROGRAM', r'program')
        self.lexer.add("ID", r'[a-zA-Z_$][a-zA-Z_0-9]*')
        self.lexer.add('COLON', r'\:')
        self.lexer.add('LEFTOP', r'\>')
        self.lexer.add('RIGHTOP', r'\<')
        self.lexer.add('NOTEQ', r'\<>')
        self.lexer.add('EQUALS', r'\=')
        self.lexer.add('SEMICOLON', r'\;')
        self.lexer.add("STRING", r"\"([^\"\\]|\\.)*\"")
        self.lexer.add('OPEN_CURLY', r'\{')
        self.lexer.add('CLOSE_CURLY', r'\}')
        self.lexer.add('COMMA', r',')
        self.lexer.add("CTE_FLOAT", r'(((0|[1-9][0-9]*)(\.[0-9]*)+)|(\.[0-9]+))([eE][\+\-]?[0-9]*)?')
        self.lexer.add('CTE_INT', r'\d+')
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
