class ASTNode:
    def __init__(self) -> None:
        self.type=None
        self.value=None
        self.child=None
        self.sibling=None
        self.sourceLineNumber=None
    
    def getName(self):
        return self.type[0]     #ast node type name
    def getPrintName(self):
        return self.type[1]    
    

    def getType(self):
        return self.type
    def setType(self,type):
        self.type=type
    def getChild(self):
        return self.child
    def setChild(self,child):
        self.child=child
    def getSibling(self):
        return self.sibling
    def setSibling(self,sibling):
        self.sibling=sibling
    def getValue(self):
        return self.value
    def setValue(self,value):
        self.value=value
    def getSourceLineNumber(self):
        return self.sourceLineNumber
    def setSourceLineNumber(self,sourceLineNumber):
        self.sourceLineNumber=sourceLineNumber


nodeTypes = {
    "IDENTIFIER": ["IDENTIFIER", "<ID:%s>"],
    "STRING": ["STRING", "<STR:'%s'>"],
    "INTEGER": ["INTEGER", "<INT:%s>"],
    "LET": ["LET", "let"],
    "LAMBDA": ["LAMBDA", "lambda"],
    "WHERE": ["WHERE", "where"],
    "TAU": ["TAU", "tau"],
    "AUG": ["AUG", "aug"],
    "CONDITIONAL": ["CONDITIONAL", "->"],
    "OR": ["OR", "or"],
    "AND": ["AND", "&"],
    "NOT": ["NOT", "not"],
    "GR": ["GR", "gr"],
    "GE": ["GE", "ge"],
    "LS": ["LS", "ls"],
    "LE": ["LE", "le"],
    "EQ": ["EQ", "eq"],
    "NE": ["NE", "ne"],
    "PLUS": ["PLUS", "+"],
    "MINUS": ["MINUS", "-"],
    "NEG": ["NEG", "neg"],
    "MULT": ["MULT", "*"],
    "DIV": ["DIV", "/"],
    "EXP": ["EXP", "**"],
    "AT": ["AT", "@"],
    "GAMMA": ["GAMMA", "gamma"],
    "TRUE": ["TRUE", "<true>"],
    "FALSE": ["FALSE", "<false>"],
    "NIL": ["NIL", "<nil>"],
    "DUMMY": ["DUMMY", "<dummy>"],
    "WITHIN": ["WITHIN", "within"],
    "SIMULTDEF": ["SIMULTDEF", "and"],
    "REC": ["REC", "rec"],
    "EQUAL": ["EQUAL", "="],
    "FCNFORM": ["FCNFORM", "function_form"],
    "PAREN": ["PAREN", "<()>"],
    "COMMA": ["COMMA", ","],
    "YSTAR": ["YSTAR", "<Y*>"],
    "BETA": ["BETA", ""],
    "DELTA": ["DELTA", ""],
    "ETA": ["ETA", ""],
    "TUPLE": ["TUPLE", ""]
}

      

# nodeTypes = {
#     "IDENTIFIER": ["IDENTIFIER"],
#     "INTEGER": ["INTEGER"],
#     "STRING": ["STRING"],
#     "LAMBDA": ["LAMBDA"],
#     "WHERE": ["WHERE"],
#     "TAU": ["TAU"],
#     "AUG": ["AUG"],
#     "CONDITIONAL": ["CONDITIONAL"],
#     "OR": ["OR"],
#     "AND": ["AND"],
#     "NOT": ["NOT"],
# }