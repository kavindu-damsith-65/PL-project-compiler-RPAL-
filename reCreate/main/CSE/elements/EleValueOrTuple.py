class EleValueOrTuple:
    def __init__(self, label):
        self.name = label

    def isLabel(self, label):
        return self.name == label

    def getLabel(self):
        return self.name
