from .ExceptionHandlerOfAST import ExceptionHandlerOfAST
from .Node import Node

class AstToSt:
  
    def expectChildren(self,node, expect):
        if not node.hasChildren(expect):
            errorMessage = f"Expected {node.getLabel()} node to have {expect} nodes"
            raise ExceptionHandlerOfAST(errorMessage)

    
    def expectMoreChildren(self,node, minimum):
        if node.getNumChild() < minimum:
            errorMessage = f"Expected {node.getLabel()} node to have at least {minimum} nodes"
            raise ExceptionHandlerOfAST(errorMessage)

    
    def checkLabel(self,node, expect):
        if not node.isLabel(expect):
            errorMessage = f"Expected {expect} node but found {node.getLabel()} node"
            raise ExceptionHandlerOfAST(errorMessage)


    def astToSt(self,node):
        node.forEachChild(self.astToSt)

        if node.isLabel("let"):
            self.checkLabel(node, "let")
            self.expectChildren(node, 2)
            eqNode = node.getChild(0)
            pNode = node.getChild(1)

            self.checkLabel(eqNode, "=")
            self.expectChildren(eqNode, 2)
            xNode = eqNode.getChild(0)
            eNode = eqNode.getChild(1)

            node.setLabel("gamma")
            eqNode.setLabel("lambda")
            node.clearChildren()
            node.addChild(eqNode)
            node.addChild(eNode)
            eqNode.clearChildren()
            eqNode.addChild(xNode)
            eqNode.addChild(pNode)
        elif node.isLabel("where"):
            self.checkLabel(node, "where")
            self.expectChildren(node, 2)
            pNode = node.getChild(0)
            eqNode = node.getChild(1)

            self.checkLabel(eqNode, "=")
            self.expectChildren(eqNode, 2)
            xNode = eqNode.getChild(0)
            eNode = eqNode.getChild(1)

            node.setLabel("gamma")
            eqNode.setLabel("lambda")
            node.clearChildren()
            node.addChild(eqNode)
            node.addChild(eNode)
            eqNode.clearChildren()
            eqNode.addChild(xNode)
            eqNode.addChild(pNode)
        elif node.isLabel("function_form"):
            self.checkLabel(node, "function_form")
            self.expectMoreChildren(node, 3)

            numberOfVNodes = node.getNumChild() - 2
            pNode = node.getChild(0)
            eNode = node.getChild(numberOfVNodes + 1)
            vNodes = [node.getChild(i + 1) for i in range(numberOfVNodes)]

            node.setLabel("=")
            node.clearChildren()
            node.addChild(pNode)
            prevNode = node
            for vNode in vNodes:
                currentNode = Node("lambda")
                prevNode.addChild(currentNode)
                currentNode.addChild(vNode)
                prevNode = currentNode
            prevNode.addChild(eNode)
        elif node.isLabel("and"):
            self.checkLabel(node, "and")
            self.expectMoreChildren(node, 2)

            numberOfEqNodes = node.getNumChild()
            eqNodes = [node.getChild(i) for i in range(numberOfEqNodes)]

            node.setLabel("=")
            node.clearChildren()
            commaNode = Node(",")
            tauNode = Node("tau")
            node.addChild(commaNode)
            node.addChild(tauNode)
            for eqNode in eqNodes:
                self.checkLabel(eqNode, "=")
                self.expectChildren(eqNode, 2)
                xNode = eqNode.getChild(0)
                eNode = eqNode.getChild(1)
                commaNode.addChild(xNode)
                tauNode.addChild(eNode)
        elif node.isLabel("rec"):
            self.checkLabel(node, "rec")
            self.expectChildren(node, 1)
            eqNode = node.getChild(0)

            self.checkLabel(eqNode, "=")
            self.expectChildren(eqNode, 2)
            xNode = eqNode.getChild(0)
            eNode = eqNode.getChild(1)

            secondXNode = xNode.copy()
            node.setLabel("=")
            node.clearChildren()
            gammaNode = Node("gamma")
            yStarNode = Node("yStar")
            lambdaNode = Node("lambda")
            node.addChild(xNode)
            node.addChild(gammaNode)
            gammaNode.addChild(yStarNode)
            gammaNode.addChild(lambdaNode)
            lambdaNode.addChild(secondXNode)
            lambdaNode.addChild(eNode)
        elif node.isLabel("lambda"):
            self.checkLabel(node, "lambda")
            self.expectMoreChildren(node, 2)

            numberOfVNodes = node.getNumChild() - 1
            vNodes = [node.getChild(i) for i in range(numberOfVNodes)]
            eNode = node.getChild(numberOfVNodes)

            currentLambdaNode = node
            currentLambdaNode.clearChildren()
            currentLambdaNode.addChild(vNodes[0])
            for vNode in vNodes[1:]:
                newLambdaNode = Node("lambda")
                currentLambdaNode.addChild(newLambdaNode)
                newLambdaNode.addChild(vNode)
                currentLambdaNode = newLambdaNode
            currentLambdaNode.addChild(eNode)
        elif node.isLabel("within"):
            self.checkLabel(node, "within")
            self.expectChildren(node, 2)
            eq1Node = node.getChild(0)
            eq2Node = node.getChild(1)

            self.checkLabel(eq1Node, "=")
            self.expectChildren(eq1Node, 2)
            self.checkLabel(eq2Node, "=")
            self.expectChildren(eq2Node, 2)
            x1Node = eq1Node.getChild(0)
            e1Node = eq1Node.getChild(1)
            x2Node = eq2Node.getChild(0)
            e2Node = eq2Node.getChild(1)

            gammaNode = Node("gamma")
            lambdaNode = Node("lambda")
            node.setLabel("=")
            node.clearChildren()
            node.addChild(x2Node)
            node.addChild(gammaNode)
            gammaNode.addChild(lambdaNode)
            gammaNode.addChild(e1Node)
            lambdaNode.addChild(x1Node)
            lambdaNode.addChild(e2Node)
            
        elif node.isLabel("@"):
            self.checkLabel(node, "@")
            self.expectChildren(node, 3)
            e1Node = node.getChild(0)
            nNode = node.getChild(1)
            e2Node = node.getChild(2)

            node.clearChildren()
            node.setLabel("gamma")
            gammaNode = Node("gamma")
            node.addChild(gammaNode)
            node.addChild(e2Node)
            gammaNode.addChild(nNode)
            gammaNode.addChild(e1Node)
