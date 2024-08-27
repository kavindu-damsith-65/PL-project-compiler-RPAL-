from exception import CustomException
from AST.ASTNode  import ASTNode
from AST.ASTNode  import nodeTypes
from collections import deque 
from AST.AST import AST
from lexicon import Token



class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.currToken = None
        self.stack = deque()

    def getNextToken(self):
        if len(self.tokens)>0:

            self.currToken = self.tokens.pop(0)
        
            if self.currToken != None:
                if self.currToken.getType() == "IDENTIFIER":
                    self.createTerminalASTNode(
                        nodeTypes["IDENTIFIER"], self.currToken.getValue())
                elif self.currToken.getType() == "INTEGER":
                    self.createTerminalASTNode(
                        nodeTypes["INTEGER"], self.currToken.getValue())
                elif self.currToken.getType() == "STRING":
                    self.createTerminalASTNode(
                        nodeTypes["STRING"], self.currToken.getValue())

    def buildAst(self):
        self.startParsing()
        return  AST(self.stack.pop())

    def startParsing(self):
        self.getNextToken()
        self.procE()
        
        # if self.currToken != None:
        #     raise CustomException("Expected EOF.")

    def createTerminalASTNode(self, type, value):
       
        node = ASTNode()
        node.setType(type)
        node.setValue(value)
        node.setSourceLineNumber(self.currToken.getLineNumber())
        self.stack.append(node)

    def createArrayAstNode(self, type, ariness):
      
        node = ASTNode()
        node.setType(type)
        # print(ariness)
        while ariness > 0:
           
            child = self.stack.pop()
            if node.getChild() != None:
                child.setSibling(node.getChild())
            node.setChild(child)
            node.setSourceLineNumber = child.getSourceLineNumber()
           
            ariness -= 1
        self.stack.append(node)

    def isCurrentToken(self, type, value):
        if self.currToken == None:
            return False
        if self.currToken.getType() != type or self.currToken.getValue() != value:
            return False
        return True

    def isCurrentTokenType(self, type):
        
        if self.currToken == None:
            return False
        if self.currToken.getType() == type:
            return True
        return False


#    * E-> 'let' D 'in' E => 'let'
#    *  -> 'fn' Vb+ '.' E => 'lambda'
#    *  -> Ew;

    def procE(self):
        
        if self.isCurrentToken("RESERVED", "let"):
            
            self.getNextToken()
            
            self.procD()
           
            
            if not self.isCurrentToken("RESERVED", "in"):
                
                raise CustomException("E:  'in' expected")
            self.getNextToken()
            self.procE()
            self.createArrayAstNode(nodeTypes["LET"], 2)

        elif self.isCurrentToken("RESERVED", "fn"):
            treesToPop = 0
            self.getNextToken()
            while self.isCurrentTokenType("IDENTIFIER") or self.isCurrentTokenType("("):
                self.procVB()
                treesToPop += 1
            if treesToPop == 0:
                raise CustomException("E: at least one 'Vb' expected")
            if not self.isCurrentToken("OPERATOR", "."):
                raise CustomException("E: '.' expected")
            self.getNextToken()
            self.procE()
            self.createArrayAstNode(nodeTypes["LAMBDA"], treesToPop+1)
        else:
            
            self.procEW()


#  * Ew -> T 'where' Dr => 'where'
#  *    -> T;

    def procEW(self):
  
        self.procT()
        if self.isCurrentToken("RESERVED", "where"):
            self.getNextToken()
            self.procDR()
            self.createArrayAstNode(nodeTypes["WHERE"], 2)


# * T -> Ta ( ',' Ta )+ => 'tau'
# *   -> Ta;

    def procT(self):
      
        self.procTA()
        treesToPop = 0
        
        while self.isCurrentToken(",", ","):
            self.getNextToken()
            self.procTA()
            treesToPop += 1
        
        if treesToPop > 0:
           
            self.createArrayAstNode(nodeTypes["TAU"], treesToPop+1)


#    * Ta -> Ta 'aug' Tc => 'aug'
#    *    -> Tc;

    def procTA(self):
       
        self.procTC()
     
        while self.isCurrentToken("RESERVED", "aug"):
            self.getNextToken()
            self.procTC()
            self.createArrayAstNode(nodeTypes["AUG"], 2)


#    * Tc -> B '->' Tc '|' Tc => '->'
#    *    -> B;

    def procTC(self):
      
        self.procB()
        if self.isCurrentToken("OPERATOR", "->"):
            self.getNextToken()
            self.procTC()
            
            if not self.isCurrentToken("OPERATOR", "|"):
                raise CustomException("TC: '|' expected")
            self.getNextToken()
            
            self.procTC()
            self.createArrayAstNode(nodeTypes["CONDITIONAL"], 3)

 # Boolean Expressions

#    * B -> B 'or' Bt => 'or'
#    *   -> Bt;

    def procB(self):
      
        self.procBT()
        while self.isCurrentToken("RESERVED", "or"):
            self.getNextToken()
            self.procBT()
            self.createArrayAstNode(nodeTypes["OR"], 2)


# * Bt -> Bs '&' Bt => '&'
# *    -> Bs;

    def procBT(self):
    
        self.procBS()
        while self.isCurrentToken("OPERATOR", "&"):
            self.getNextToken()
            self.procBS()
            self.createArrayAstNode(nodeTypes["AND"], 2)


# * Bs -> 'not Bp => 'not'
# *    -> Bp;

    def procBS(self):
   
        if self.isCurrentToken("RESERVED", "not"):
            self.getNextToken()
            self.procBP()
            self.createArrayAstNode(nodeTypes["NOT"], 1)
        else:
            self.procBP()


#    * Bp -> A ('gr' | '>' ) A => 'gr'
#    *    -> A ('ge' | '>=' ) A => 'ge'
#    *    -> A ('ls' | '<' ) A => 'ge'
#    *    -> A ('le' | '<=' ) A => 'ge'
#    *    -> A 'eq' A => 'eq'
#    *    -> A 'ne' A => 'ne'
#    *    -> A;

# check aain

    def procBP(self):
      
        self.procA()
        
        if self.isCurrentToken("RESERVED", "gr") or self.isCurrentToken("OPERATOR", ">"):
            self.getNextToken()
            self.procA()
            self.createArrayAstNode(nodeTypes["GR"], 2)
        elif self.isCurrentToken("RESERVED", "ge") or self.isCurrentToken("OPERATOR", ">="):
            self.getNextToken()
            self.procA()
            self.createArrayAstNode(nodeTypes["GE"], 2)
        elif self.isCurrentToken("RESERVED", "ls") or self.isCurrentToken("OPERATOR", "<"):
            self.getNextToken()
            self.procA()
            self.createArrayAstNode(nodeTypes["LS"], 2)
        elif self.isCurrentToken("RESERVED", "le") or self.isCurrentToken("OPERATOR", "<="):
            self.getNextToken()
            self.procA()
            self.createArrayAstNode(nodeTypes["LE"], 2)
        elif self.isCurrentToken("RESERVED", "eq"):
            self.getNextToken()
            self.procA()
            self.createArrayAstNode(nodeTypes["EQ"], 2)
        elif self.isCurrentToken("RESERVED", "ne"):
            self.getNextToken()
            self.procA()
            self.createArrayAstNode(nodeTypes["NE"], 2)


# Arithmetic Expressions
#    * A -> A '+' At => '+'
#    *   -> A '-' At => '-'
#    *   ->   '+' At
#    *   ->   '-' At => 'neg'
#    *   -> At;

    def procA(self):
       
        if self.isCurrentToken("OPERATOR", "+"):
            self.getNextToken()
            self.procAT()
        elif self.isCurrentToken("OPERATOR", "-"):
            self.getNextToken()
            self.procAT()
            self.createArrayAstNode("NEG", 1)
        else:
            self.procAT()

        plus = True
        while self.isCurrentToken("OPERATOR", "+") or self.isCurrentToken("OPERATOR", "-"):
            if self.currToken.getValue() == "+":
                plus = True
            elif self.currToken.getValue() == "-":
                plus = False
            self.getNextToken()
            self.procAT()
            if plus:
                self.createArrayAstNode(nodeTypes["PLUS"], 2)
            else:
                self.createArrayAstNode(nodeTypes["MINUS"], 2)


#    * At -> At '*' Af => '*'
#    *    -> At '/' Af => '/'
#    *    -> Af;


    def procAT(self):
       
        self.procAF()
        mult = True
        while self.isCurrentToken("OPERATOR", "*") or self.isCurrentToken("OPERATOR", "/"):
            if self.currToken.getValue() == "*":
                mult = True
            elif self.currToken.getValue() == "/":
                mult = False
            self.getNextToken()
            self.procAF()
            if mult:
                self.createArrayAstNode(nodeTypes["MULT"], 2)
            else:
                self.createArrayAstNode(nodeTypes["DIV"], 2)


#    * Af -> Ap '**' Af => '**'
#    *    -> Ap;

    def procAF(self):
     
        self.procAP()
        
        if self.isCurrentToken("OPERATOR", "**"):
            self.getNextToken()
            self.procAF()
            self.createArrayAstNode(nodeTypes["EXP"], 2)

#    * Ap -> Ap '@' '&lt;IDENTIFIER&gt;' R => '@'
#    *    -> R;
    def procAP(self):
        
        self.procR()
        while self.isCurrentToken("OPERATOR", "@"):
            self.getNextToken()
            if not self.isCurrentTokenType("IDENTIFIER"):
                raise CustomException("AP: expected Identifier")
            self.getNextToken()
            self.procR()
            self.createArrayAstNode(nodeTypes["AT"], 3)


# Rators and Rands

# * R -> R Rn => 'gamma'
# *   -> Rn;
    def procR(self):
       
        self.procRN() 
        self.getNextToken()
        

        
        while (self.isCurrentTokenType("INTEGER") or
            self.isCurrentTokenType("STRING") or
            self.isCurrentTokenType("IDENTIFIER") or
            self.isCurrentToken("RESERVED", "true") or
            self.isCurrentToken("RESERVED", "false") or
            self.isCurrentToken("RESERVED", "nil") or
            self.isCurrentToken("RESERVED", "dummy") or self.isCurrentTokenType("(")): 
            
            self.procRN()
            
            self.createArrayAstNode(nodeTypes['GAMMA'], 2)
            self.getNextToken() 


#    * Rn -> '&lt;IDENTIFIER&gt;'
#    *    -> '&lt;INTEGER&gt;'
#    *    -> '&lt;STRING&gt;'
#    *    -> 'true' => 'true'
#    *    -> 'false' => 'false'
#    *    -> 'nil' => 'nil'
#    *    -> '(' E ')'
#    *    -> 'dummy' => 'dummy'
    def procRN(self):
      
        if self.isCurrentTokenType("IDENTIFIER") or  self.isCurrentTokenType("INTEGER") or self.isCurrentTokenType("STRING"):
            pass
        elif self.isCurrentToken("RESERVED", "true"):
            self.createTerminalASTNode(nodeTypes["TRUE"], "true")
        elif self.isCurrentToken("RESERVED", "false"):
            self.createTerminalASTNode(nodeTypes["FALSE"], "false")
        elif self.isCurrentToken("RESERVED", "nil"):
            self.createTerminalASTNode(nodeTypes["NIL"], "nil")
        elif self.isCurrentTokenType("("):
            self.getNextToken()
            
            self.procE()
            if not self.isCurrentTokenType(")"):
                raise CustomException("RN: ')' expected")
        elif self.isCurrentToken("RESERVED", "dummy"):
            self.createTerminalASTNode(nodeTypes["DUMMY"], "dummy")





#######################################   Definitions
            
# * D -> Da 'within' D => 'within'
# *   -> Da;
    def procD(self):
      
        self.procDA()
        if self.isCurrentToken("RESERVED","within"):
            self.getNextToken()
            self.procD()
            self.createArrayAstNode(nodeTypes["WITHIN"],2)
        

#  * Da -> Dr ('and' Dr)+ => 'and'
#  *    -> Dr;
    def procDA(self):
       
        self.procDR()
        treesToPop=0
        while self.isCurrentToken("RESERVED","and"):
            self.getNextToken()
            self.procDR()
            treesToPop+=1
        if treesToPop>0:
            self.createArrayAstNode(nodeTypes["SIMULTDEF"],treesToPop+1)


# * Dr -> 'rec' Db => 'rec'
# * -> Db;
    def procDR(self):
       
        if self.isCurrentToken("RESERVED","rec") :
            self.getNextToken()
            self.procDB()
            self.createArrayAstNode(nodeTypes["REC"],1)
        else:
            self.procDB()

# * Db -> Vl '=' E => '='
# *    -> '&lt;IDENTIFIER&gt;' Vb+ '=' E => 'fcn_form'
# *    -> '(' D ')';   

    def procDB(self):
       
        if self.isCurrentTokenType("("):
            self.procD()
            self.getNextToken()
            if not self.isCurrentTokenType(")"):
                raise CustomException("DB: ')' expected")
            self.getNextToken()
        elif self.isCurrentTokenType("IDENTIFIER"):
            self.getNextToken()
            if self.isCurrentToken(",", ","):
                self.getNextToken()
                self.procVL()

                if not self.isCurrentToken("OPERATOR", "="):
                    raise CustomException("DB: = expected.")
                self.createArrayAstNode(nodeTypes["COMMA"], 2)
                self.getNextToken()
                self.procE()
                self.createArrayAstNode(nodeTypes["EQUAL"], 2)
            else:
                if self.isCurrentToken("OPERATOR", "="):
                    self.getNextToken()
                    self.procE()
                    self.createArrayAstNode(nodeTypes["EQUAL"], 2)
                else:
                    treesToPop = 0

                    while self.isCurrentTokenType("IDENTIFIER") or self.isCurrentTokenType("("):
                        self.procVB()
                        treesToPop += 1

                    if treesToPop == 0:
                        raise CustomException("E: at least one 'Vb' expected")

                    if not self.isCurrentToken("OPERATOR", "="):
                        raise CustomException("DB: = expected.")

                    self.getNextToken()
                    self.procE()
                   
                   
                    self.createArrayAstNode(nodeTypes["FCNFORM"], treesToPop + 2)




#############################    Variables
                    

#    * Vb -> '&lt;IDENTIFIER&gt;'
#    *    -> '(' Vl ')'
#    *    -> '(' ')' => '()'   
    def procVB(self):
    
        if self.isCurrentTokenType("IDENTIFIER"):
            self.getNextToken()
        elif self.isCurrentTokenType("("):
            self.getNextToken()
            if self.isCurrentTokenType(")"):
                self.createTerminalASTNode(nodeTypes["PAREN"], "")
                self.getNextToken()
            else:
                self.procVL()
                if not self.isCurrentTokenType(")"):
                    
                    raise CustomException("VB: ')' expected")
                self.getNextToken()

    def procVL(self):
       
        if not self.isCurrentTokenType("IDENTIFIER"):
            raise CustomException("VL: Identifier expected")
        else:
            self.getNextToken()
            
            treesToPop = 0
            while self.isCurrentToken(",", ","):
               
                self.getNextToken()
                if not self.isCurrentTokenType("IDENTIFIER"):
                    raise CustomException("VL: Identifier expected")
                self.getNextToken()
                treesToPop += 1
            if treesToPop > 0:
                
                self.createArrayAstNode(nodeTypes["COMMA"], treesToPop + 1) 
            


