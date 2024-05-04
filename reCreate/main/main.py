from lexicon import *
from parser1 import Parser
from exception import CustomException
import sys

if __name__ == "__main__":
    fileName=sys.argv[1:]
    tokens=[]
    with open(fileName[0], "r") as file:
        lines=file.readlines()
        tokens=get_next_token(lines,tokens)
        # print("[",end="")
        # for i in tokens:
        #     # print("Token:", i.type, "Value:", i.value)
        #      print('Token("%s","%s",1),' % (i.type,i.value))
        # print("]",end="")
        try:
            pasrser = Parser(tokens)
            ast=pasrser.buildAst()
            print(ast.getAST())
    
        except CustomException as e:
            print("Custom Exception:", e.message)