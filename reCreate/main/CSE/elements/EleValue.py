from .EleValueOrTuple import EleValueOrTuple
from INTERPRETER.Node import Node
 
class EleValue(EleValueOrTuple):
    def __init__(self, type, value=None):
        if isinstance(type, str):
             super().__init__(type)
             self.value = value
        if isinstance(type, Node):
            super().__init__(type.getLabel())
            self.value = type.getValue()

    def getValue(self):
        return self.value

    def equals(self, o):
        if self is o:
            return True
        if o is None or self.__class__ != o.__class__:
            return False
        return self.value == o.value

    def hashCode(self):
        return hash(self.value)

    def toString(self):
        if self.value is None:
            return self.getLabel()
        return f"{self.getLabel()}({self.getValue()})"
