from lexer import Lexer
from parser import Parser

def analyzeCode(input):
    lexer = Lexer().get_lexer()
    tokens = lexer.lex(input)

    pg = Parser()
    pg.parse()
    parser = pg.get_parser()
    for token in lexer.lex(input):
        print(token)
    try:
        if(parser.parse(tokens).eval()):
            print("Programa Valido")
    except Exception as ex:
          print("Programa Invalido", ex)

def inputUser():
     archName = "correct.txt"
     file = open(archName, "r", encoding="utf-8")
     user_input = file.read()
     return user_input

def main():
    correct_test = inputUser()
    analyzeCode(correct_test)

if __name__=='__main__':
     main()# Stack example