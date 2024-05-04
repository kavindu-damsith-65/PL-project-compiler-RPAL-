from collections import deque

from .elements.EleValue import EleValue
from ..INTERPRETER.Node import Node


class ElementParser:
    @staticmethod
    def generateCs(root):
        controls = []
        control = deque()
        controls.append(control)
        ElementParser.generateCS(root, controls, control)
        return controls

    @staticmethod
    def generateCS(node, controls, currentControl):
        if node.isLabel("lambda"):
            ElementParser.generateCsLambda(node, controls, currentControl)
        elif node.isLabel("->"):
            ElementParser.generateCsIf(node, controls, currentControl)
        elif node.isLabel("tau"):
            ElementParser.generateCsTau(node, controls, currentControl)
        else:
            # Add this node and recurse on children
            currentControl.append(EleValue(node))

            node.forEachChild(lambda child :ElementParser.generateCS(child, controls, currentControl) )
          

    @staticmethod
    def generateCsLambda(node, controls, currentControl):
        # Get right and left children
        newIndex = len(controls)
        leftChild = node.getChild(0)
        rightChild = node.getChild(1)

        if leftChild.isLabel(","):
            children = []
            leftChild.forEachChild(lambda child :children.append(child.getValue())) 
            combinedParams = ",".join(children)
            leftChild = Node("id", combinedParams)

        # Control element
        controlValue = f"{newIndex} {leftChild.getValue()}"
        newControlElem = EleValue("lambda", controlValue)
        currentControl.append(newControlElem)

        # New control structure
        newControl = deque()
        controls.append(newControl)

        # Traverse in new structure
        ElementParser.generateCS(rightChild, controls, newControl)

    @staticmethod
    def generateCsIf(node, controls, currentControl):
        conditionNode = node.getChild(0)
        thenNode = node.getChild(1)
        elseNode = node.getChild(2)

        thenIndex = len(controls)
        thenElem = EleValue("delta", str(thenIndex))
        currentControl.append(thenElem)
        thenControl = deque()
        controls.append(thenControl)
        ElementParser.generateCS(thenNode, controls, thenControl)

        elseIndex = len(controls)
        elseElem = EleValue("delta", str(elseIndex))
        currentControl.append(elseElem)
        elseControl = deque()
        controls.append(elseControl)
        ElementParser.generateCS(elseNode, controls, elseControl)

        currentControl.append(EleValue("beta"))
        ElementParser.generateCS(conditionNode, controls, currentControl)

    @staticmethod
    def generateCsTau(node, controls, currentControl):
        currentControl.append(EleValue("tau", str(node.getNumChild())))
        node.forEachChild(lambda child :ElementParser.generateCS(child, controls, currentControl) )

       