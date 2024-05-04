from collections import deque

from .elements.EleValue import EleValue
from INTERPRETER.Node import Node


class ElementParser:
    
    def generateCs(self,node,controls=None, currentControl=None):
        if not controls:
            controls = []
            control = deque()
            controls.append(control)
            self.generateCs(node, controls, control)
            return controls
        
        else:
            if node.isLabel("lambda"):
                self.generateCsLambda(node, controls, currentControl)
            elif node.isLabel("->"):
                self.generateCsIf(node, controls, currentControl)
            elif node.isLabel("tau"):
                self.generateCsTau(node, controls, currentControl)
            else:
                # Add this node and recurse on children
                currentControl.append(EleValue(node))

                node.forEachChild(lambda child :self.generateCs(child, controls, currentControl) )
    
          
    
    def generateCsLambda(self,node, controls, currentControl):
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
        self.generateCs(rightChild, controls, newControl)

    
    def generateCsIf(self,node, controls, currentControl):
        conditionNode = node.getChild(0)
        thenNode = node.getChild(1)
        elseNode = node.getChild(2)

        thenIndex = len(controls)
        thenElem = EleValue("delta", str(thenIndex))
        currentControl.append(thenElem)
        thenControl = deque()
        controls.append(thenControl)
        self.generateCs(thenNode, controls, thenControl)

        elseIndex = len(controls)
        elseElem = EleValue("delta", str(elseIndex))
        currentControl.append(elseElem)
        elseControl = deque()
        controls.append(elseControl)
        self.generateCs(elseNode, controls, elseControl)

        currentControl.append(EleValue("beta"))
        self.generateCs(conditionNode, controls, currentControl)

    
    def generateCsTau(self,node, controls, currentControl):
        currentControl.append(EleValue("tau", str(node.getNumChild())))
        node.forEachChild(lambda child :self.generateCs(child, controls, currentControl) )

       