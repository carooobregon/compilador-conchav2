from rply import ParserGenerator
import pprint

pp = pprint.PrettyPrinter(indent=4)

class symbolTable:
    def __init__(self):
        self.functions={}
    