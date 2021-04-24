from lexer import Lexer
from parser import Parser
from pathlib import Path

def analyzeCode(input):
    lexer = Lexer().get_lexer()
    tokens = lexer.lex(input)

    pg = Parser()
    pg.parse()
    parser = pg.get_parser()
    # for token in lexer.lex(input):
    #     print(token)
    try:
        if(parser.parse(tokens)):
            print("Shes very gorgeous to me!")
    except Exception as ex:
          print("vibes are off bro", ex)

def inputUser():
     data_folder = Path("../tests/")
     file_to_open = data_folder / "correct.txt"
     file = open(file_to_open)
     user_input = file.read()
     return user_input

def main():
    correct_test = inputUser()
    analyzeCode(correct_test)

if __name__=='__main__':
     main()# Stack example