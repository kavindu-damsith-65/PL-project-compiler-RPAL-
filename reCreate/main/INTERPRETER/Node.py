class Node:
   
    def __init__(self, label, value=None):
        self.children = []
        self.parent = None
        self.label = label
        self.value = value

    def copy(self):
        copied = Node(self.label, self.value)
        for child in self.children:
            copied.addChild(child.copy())
        return copied

    def getParent(self):
        return self.parent

    def getLabel(self):
        return self.label

    def getValue(self):
        return self.value

    def getNumChild(self):
        return len(self.children)

    def hasChildren(self, n):
        return len(self.children) == n

    def isLabel(self, label):
        return self.getLabel() == label

    def getChild(self, i):
        return self.children[i]

    def forEachChild(self, action):
        for child in self.children:
            action(child)

    def setLabel(self, label):
        self.label = label
        self.value = None

    def clearChildren(self):
        for child in self.children:
            child.parent = None
        self.children.clear()

    def addChild(self, child):
        self.children.append(child)
        child.parent = self
