from .Node import Node

class DepthOfNode(Node):
    def __init__(self, parent, label, depth,value=None):
        if not value:
            super().__init__(label)
            self.depth = depth
            if parent is not None:
                parent.addChild(self)
        else:
            super().__init__(label, value)
            self.depth = depth
            if parent is not None:
                parent.addChild(self)


    def getDepth(self):
        return self.depth

    def getParent(self):
        return super().getParent()
