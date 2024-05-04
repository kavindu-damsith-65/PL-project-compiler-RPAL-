from .DepthOfNode import DepthOfNode

class CreateTree:
    def nodeFromFile(self,astTexStrings):
        lines = astTexStrings

        root = None
        parent = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            data = ""
            for i in range(len(line)):
                c = line[i]
                if c != '.':
                    data = line[i:]
                    break

            currentDepth = len(line) - len(data)
            if currentDepth == 0 and root is not None:
                break
            while parent is not None and parent.getDepth() >= currentDepth:
                parent = parent.getParent()

            node=None
            if data.startswith("<") and data.endswith(">"):
                label=None
                value=None
                if ":" in data:
                    borderPos = data.index(':')
                    label = data[1:borderPos].lower()
                    if label == "str":
                        value = data[borderPos + 2:-2]
                        value = self.getJavaValue(value)
                    else:
                        value = data[borderPos + 1:-1]
                    # node = DepthOfNode(parent, label, value, currentDepth)
                else:
                    label = data[1:-1].lower()
                    value = None
                node = DepthOfNode(parent, label, currentDepth,value)
            else:
                node = DepthOfNode(parent, data, currentDepth)

            if parent is None:
                root = node
            parent = node

        return root

   
    def getJavaValue(self,st):
        stringBuilder = ""
        ele = 0

        while ele < len(st):
            character = st[ele]
            if character == '\\':
                nextCharacter = '\\' if ele == len(st) - 1 else st[ele + 1]
                if nextCharacter >= '0' and nextCharacter <= '7':
                    code = nextCharacter
                    ele += 1
                    if ele < len(st) - 1 and st[ele + 1] >= '0' and st[ele + 1] <= '7':
                        code += st[ele + 1]
                        ele += 1
                        if ele < len(st) - 1 and st[ele + 1] >= '0' and st[ele + 1] <= '7':
                            code += st[ele + 1]
                            ele += 1
                    stringBuilder += chr(int(code, 8))
                    continue
                if nextCharacter == '\\':
                    character = '\\'
                elif nextCharacter == 'b':
                    character = '\b'
                elif nextCharacter == 'f':
                    character = '\f'
                elif nextCharacter == 'n':
                    character = '\n'
                elif nextCharacter == 'r':
                    character = '\r'
                elif nextCharacter == 't':
                    character = '\t'
                elif nextCharacter == '\"':
                    character = '\"'
                elif nextCharacter == '\'':
                    character = '\''
                elif nextCharacter == 'u':
                    if ele >= len(st) - 5:
                        character = 'u'
                    code = int(st[ele + 2:ele + 6], 16)
                    stringBuilder += chr(code)
                    ele += 5
                    continue
                ele += 1
            stringBuilder += character
            ele += 1

        return stringBuilder

