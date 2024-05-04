from .EleValueOrTuple import EleValueOrTuple

class EleTuple(EleValueOrTuple):
    def __init__(self, value):
        super().__init__("tuple")
        self.value = value

    def getValue(self):
        return self.value

    def equals(self, o):
        if self is o:
            return True
        if o is None or self.__class__ != o.__class__:
            return False
        return self.value == o.value

    def hashCode(self):
        return hash(tuple(self.value))

    def toString(self):
        return str(self.value)


