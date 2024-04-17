import sys

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
            if not isSpace(line) and not isComment(line):
                lists.append(line)
    return lists

def isPreDefineSymbol(symbols):
    return False

def isComment(lines):
    return "//" in lines

def isSpace(lines):
    return lines.isspace()

# return the type of the current instruction,
# @xxx is A, 
def instructionType(line):
    if "@" in line:
        return A_INSTRUCTION
    if line in SYMBOL_TABLE:
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
    return str(JUMP[line_jump])

def decimal_to_binary(n):
    to_int = int(n)
    tmp = str(bin(to_int)[2:])
    while len(tmp) < 15:
        tmp = "0" + tmp
    return tmp

def symbolToNumber(symbol):
    if symbol in SYMBOL_TABLE:
        return SYMBOL_TABLE[symbol]
    else:
        SYMBOL_TABLE[symbol] = str(len(SYMBOL_TABLE))

alists = initializer(sys.argv[1])

def assembler(alist):
    binlist = []
    for l in alist:
        l = l[:-1]
        if instructionType(l) >= 0:
            tmp = "0" + decimal_to_binary(l[1:])
            binlist.append(tmp)
        else:
            print(l)
            binlist.append("111" + separetIns(l))
            
    return binlist
            

def separetIns(line):
    tmp = []
    dest_part = ""
    comp_part= ""
    jump_part = ""
    #print("DEBUG:",line)
    if "=" in line:
        a,b = line.split("=", 1)
        dest_part = dest(a)
        print("dest:", dest_part)
    
    comp_part = comp(b)
    print("comp:", comp_part)
    jump_part = jump("null")
    print("jump:", jump_part)
    whole = comp_part + dest_part + jump_part
    return whole
        

hack_code = assembler(alists)
with open("Add.hack", "a") as f:
    for code in hack_code:
        print(code, file=f)
