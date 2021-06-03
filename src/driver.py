from Parser.lexer import Lexer
from Parser.parser import Parser
from VirtualMachine.virtualmachine import VirtualMachine
from pathlib import Path

class Driver:
    def __init__(self):
        self.vm = VirtualMachine()
        pass
    
    def compileAndRun(self, input):
        if self.analyzeCode(input):
            self.runCode()
        
    def analyzeCode(self,input):
        lexer = Lexer().get_lexer()
        tokens = lexer.lex(input)
        pg = Parser()
        pg.parse()
        parser = pg.get_parser()
        try:
            parser.parse(tokens)
            return True
        except Exception as ex:
            print("vibes are off bro", ex)
            return False

    def runCode(self):
        self.vm.runVM()