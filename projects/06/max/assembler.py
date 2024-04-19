import sys

counter = 0
SYMBOL_TABLE = {
        "R0": "0",
        "R1": "1",
        "R2": "2",
        "R3": "3",
        "R4": "4",
        "R5": "5",
        "R6": "6",
        "R7": "7",
        "R8": "8",
        "R9": "9",
        "R10": "10",
        "R11": "11",
        "R12": "12",
        "R13": "13",
        "R14": "14",
        "R15": "15",
        "SCREEN": "16384",
        "KBD": "24576",
        "SP": "0", 
        "LCL": "1",
        "ARG": "2",
        "THIS": "3",
        "THAT": "4"
        }

JUMP = {
        "null":"000",
        "JGT":"001",
        "JEQ":"010",
        "JGE":"011",
        "JLT":"100",
        "JNE":"101",
        "JLE":"110",
        "JMP":"111"
        }

DEST = {
        "null":"000",
        "M":"001",
        "D":"010",
        "MD":"011",
        "DM":"011",
        "A":"100",
        "AM":"101",
        "AD":"110",
        "AMD":"111"
        }

COMP = {
        "0":"101010",
        "1":"111111",
        "-1":"111010",
        "D":"001100",
        "A":"110000",
        "M":"110000",
        "!D":"001101",
        "!A":"110001",
        "!M":"110001",
        "-D":"001111",
        "-A":"110011",
        "-M":"110011",
        "D+1":"011111",
        "A+1":"110111",
        "M+1":"110111",
        "D-1":"001110",
        "A-1":"110010",
        "M-1":"110010",
        "D+A":"000010",
        "D+M":"000010",
        "D-A":"010011",
        "D-M":"010011",
        "A-D":"000111",
        "M-D":"000111",
        "D&A":"000000",
        "D&M":"000000",
        "D|A":"010101",
        "D|M":"010101"
        }

A_INSTRUCTION = 1
L_INSTRUCTION = 0
C_INSTRUCTION = -1

def initializer(file):
    lists = []
    with open(file, 'r') as f:
        for line in f:
            line = removeSpace(line)
            line = removeComment(line)
            line = line.replace('\n','')
            if not isSpace(line) and not isEmptyLine(line):
                lists.append(line)
    return lists

def isPreDefineSymbol(symbols):
    return False

def isComment(lines):
    return "//" in lines

def isEmptyLine(line):
    if line == "":
        return True
    return False

def removeComment(lines):
    if not isComment(lines):
        return lines
    tmp = lines.split("//")[0]
    return tmp

def removeSpace(lines):
    return lines.replace(" ", "")

def removeBrackets(lines):
    tmp = removeSpace(lines)
    tmp = tmp[1:-1]
    return tmp

def isSpace(lines):
    return lines.isspace()

# return the type of the current instruction,
# @xxx is A, 
def instructionType(line):
    if "@" in line:
        return A_INSTRUCTION
    if "(" in line:
        return L_INSTRUCTION
    return C_INSTRUCTION

# if the current instruction is (xxx), returns the symbol xxx
# if the current instruction is @xxx, returns the symbol or decimal xxx(as a string).
def symbol(instruction):
    if "@" in instruction:
        return instruction[1:]
    return instruction

# Returns the symbolic dest part of the current C-instruction, Should be called only if instructionType is C
def dest(line_dest):
    if line_dest == "":
        return str(DEST["null"])
    return str(DEST[line_dest])

# Returns the symbolic comp part of the current C-instruction
def comp(line_comp):
    tmp = ""
    if "M" in line_comp:
        tmp = tmp + "1"
    else:
        tmp = tmp + "0"
    tmp = tmp + COMP[line_comp]
    return tmp

# Returns the symbolic jump part of the current C-instruction
def jump(line_jump):
    if line_jump == "":
        return str(JUMP["null"])
    return str(JUMP[line_jump])

def decimal_to_binary(n):
    to_int = int(n)
    tmp = str(bin(to_int)[2:])
    while len(tmp) < 15:
        tmp = "0" + tmp
    return tmp

# Returns the address of the symbol
def symbolToNumber(symbol):
    print("symbolToNumber:", symbol)
    address = len(SYMBOL_TABLE) - 7
    i = '('+symbol+')'
    print(i)
    if i in alists and symbol not in SYMBOL_TABLE:
        SYMBOL_TABLE[str(symbol)] = str(alists.index(i))
        alists.remove(i)
    elif symbol not in SYMBOL_TABLE:
        SYMBOL_TABLE[str(symbol)] = str(address)
        return address
    return SYMBOL_TABLE[symbol]

alists = initializer(sys.argv[1])

def assembler(alist):
    global counter 
    binlist = []
    for l in alist:
        insType = instructionType(l)
        #print("l:", l)
        #print("type:", insType)
        if insType == 1: # A instruction
            tmp = getAIns(l)
            binlist.append(tmp)
            counter = counter + 1
        elif insType == 0: # L instruction
            addLIns(l)
        elif insType == -1: # C instruction
            binlist.append(getCIns(l))
            counter = counter + 1
        #print("counter:", counter)
    return binlist
            

def getAIns(line):
    item = line[1:]
    aBinary = "0" + decimal_to_binary(symbolToNumber(item))
    #print("AB:", aBinary)
    return aBinary

def addLIns(line):
    global counter
    item = removeBrackets(line)
    if item not in SYMBOL_TABLE:
        print("item:", item, "counter", counter)
        SYMBOL_TABLE[str(item)] = str(counter)

def getCIns(line):
    #print("getC", line)
    return "111" + separetIns(line)
            

def separetIns(line):
    tmp = []
    dest_part = ""
    comp_part= ""
    jump_part = ""
    if "=" in line:
        dest_part, comp_part = line.split("=")
        #print("dest_part", dest_part)
        #print("comp_part", comp_part)
        dest_part = dest(dest_part)
        jump_part = jump(jump_part)
        comp_part = comp(comp_part)
        #print("dest:", dest_part)
        #print("comp:", comp_part)
    elif ";" in line:
        comp_part, jump_part = line.split(";")
        dest_part = dest(dest_part)
        comp_part = comp(comp_part)
        jump_part = jump(jump_part)
        #print("jump:", jump_part)
    whole = comp_part + dest_part + jump_part
    #print("whole:", whole)
    return whole
        

hack_code = assembler(alists)
with open("foo.hack", "a") as f:
    for code in hack_code:
        print(code, file=f)

# 1. deal with symbols ,like "(LOOP)" symbol
# 2. separet C instruction
# 3. remember the address
# 4. remove comments
