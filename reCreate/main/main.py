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
    astVisible=False
    
    params=sys.argv[1:]
    if len(params)==1:
        path=params[0]
    elif len(params) ==2 and params[0]=="--ast":
        astVisible=True
        path=params[1]

        
    tokens=[]
    with open(path, "r") as file:
    # with open("defns.1", "r") as file:
       
        # print("[",end="")
        # for i in tokens:
        #     # print("Token:", i.type, "Value:", i.value)
        #      print('Token("%s","%s",1),' % (i.type,i.value))
        # print("]",end="")
        try:
            lines=file.readlines()
            tokens=get_next_token(lines,tokens)
            pasrser = Parser(tokens)
            ast=pasrser.buildAst()

            if astVisible:    
               print(ast.getAST())
               print("")
            

            text =ast.getAST().split("\n")
            root=CreateTree().nodeFromFile(text)
            AstToSt().astToSt(root)
            controls=ElementParser().generateCs(root)
            cseMachine=CSEMachine(controls)
            cseMachine.evaluateTree()

       
        except CustomException as e:
            print("Custom Exception:", e.message)
        except ExceptionHandlerOfAST as e:
            print("Custom Exception:", e.message)
        except ExceptionHandlerOfCSE as e:
            print("Custom Exception:", e.message)
        except RuntimeError as e:
            print("Custom Exception:", e.message)
        
    