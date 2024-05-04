from lexicon import *
from parser1 import Parser
from exception import CustomException
from INTERPRETER.ExceptionHandlerOfAST import ExceptionHandlerOfAST
from CSE.ExceptionHandlerOfCSE import ExceptionHandlerOfCSE
from CSE.ElementParser import ElementParser
from CSE.CSEMachine import CSEMachine
from INTERPRETER.createTree import CreateTree
from INTERPRETER.ASTtoST import AstToSt
import sys

if __name__ == "__main__":
    fileName=sys.argv[1:]
    tokens=[]
    # with open(fileName[0], "r") as file:
    with open("defns.1", "r") as file:

        lines=file.readlines()
        tokens=get_next_token(lines,tokens)
        # print("[",end="")
        # for i in tokens:
        #     # print("Token:", i.type, "Value:", i.value)
        #      print('Token("%s","%s",1),' % (i.type,i.value))
        # print("]",end="")
        # try:
        pasrser = Parser(tokens)
        ast=pasrser.buildAst()
        # print(ast.getAST())
        # try:

        text =ast.getAST().split("\n")
        root=CreateTree().nodeFromFile(text)
        AstToSt().astToSt(root)
        controls=ElementParser().generateCs(root)
        cseMachine=CSEMachine(controls)
        cseMachine.evaluateTree()

    
        # except CustomException as e:
        #     print("Custom Exception:", e.message)
        # except ExceptionHandlerOfAST as e:
        #     print("Custom Exception:", e.message)
        # except ExceptionHandlerOfAST as e:
        #     print("Custom Exception:", e.message)
        # except RuntimeError as e:
        #     print("Custom Exception:", e.message)
        
    