from .ASTNode import nodeTypes

class AST:
    def __init__(self,root) -> None:
        self.text=""
        self.root=root
    def getAST(self):
       self.preOrder(self.root,"")
       return self.text
    def preOrder(self,node,printPrefix):
        if node==None:
            return
        self.addNodeDetails(node,printPrefix)
        self.preOrder(node.getChild(),printPrefix+".")
        self.preOrder(node.getSibling(),printPrefix)

    def addNodeDetails(self,node,printPrefix):
        # print("tempdddddd",node.getType())
        if node.getType()[0]==nodeTypes["IDENTIFIER"][0] or node.getType()[0]==nodeTypes["INTEGER"][0]:
           
            string=str(printPrefix+node.getPrintName()+"\n") % (node.getValue())
            self.text+=string
        elif node.getType()[0]==nodeTypes["STRING"][0]:
            string=str(printPrefix+node.getPrintName()+"\n") % (node.getValue())
            self.text+=string
        else:
            self.text+=printPrefix+node.getPrintName()+"\n"
