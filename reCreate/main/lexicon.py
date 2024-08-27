import re
reservedIdentifiers=["let","in","within","fn","where","aug","or","not","gr","ge","ls","le","eq","ne","true", "false","nil","dummy","rec","and"]


class Token:
    def __init__(self, type, value,line):
        self.type = type
        self.value = value
        self.tokenLine=line

    def getType(self):
        return self.type
    def getValue(self):
        return self.value
    def getLineNumber(self):
        return self.tokenLine



def is_letter(line):
    match =re.search(r'^[A-Za-z0-9\_]+', line)
    return match

def is_digit(line):
    match =re.search(r'^[0-9]+', line)
    return match

def is_operator(line):
    match =re.search(r"^[+\-\*/<>&\.@/:=~\|\$\[!\]\#\%^_\[\]\{\}]+", line)
    return match 

def is_punctuation(line):
    match =re.search(r'^[\(\)\;\,]', line)
    return match


def is_string(line):
    # match =re.search(r'^\'(\w|\d)*\'', line)
    # stringPattern=r"^\'(\t|\n|\\||\(|\)|\;|\,|[A-Za-z0-9+\-*/<>&\.@/:=~|\$\[!\]\#\%^_\[\]\{\}])*\'"
    stringPattern=r"^\'[^']*\'"
    match =re.search(stringPattern, line)
    return match


def is_removeable(line):
    match =re.search(r"^(?://.*\n|[\t\n\r])", line)
    return match

def get_next_token(lines,tokens):
    global reservedIdentifiers
    for index,line in enumerate(lines):
        while line:
           
            line=line.strip()
            match=is_letter(line)
            
            if match:
                if match.group().strip() in reservedIdentifiers:
                    token = Token("RESERVED", match.group().strip(),index)
                else:
                    token = Token("IDENTIFIER", match.group().strip(),index)
                tokens.append(token)
                line=line[match.end():]
                continue

            match=is_digit(line)
            
            if match:
                token = Token("INTEGER", match.group().strip(),index)
                tokens.append(token)
                line=line[match.end():]
                continue

            
            match=is_operator(line)
            if match:
                token = Token("OPERATOR", match.group().strip(),index)
                tokens.append(token)
                line=line[match.end():]
                continue

            match=is_string(line)
            if match:
                token = Token("STRING", match.group().strip(),index)
                tokens.append(token)
                line=line[match.end():]
                continue


            match=is_punctuation(line)
            if match:
                token=None
                # if match.group().strip()==";" or match.group().strip()==",":
                #     token = Token("OPERATOR", match.group().strip(),index)
                # else:
                token = Token(match.group().strip(), match.group().strip(),index)
                tokens.append(token)
                line=line[match.end():]
                continue
            
            match=is_removeable(line)
            if match:
                line=line[match.end():]
                continue
        
    return tokens


   