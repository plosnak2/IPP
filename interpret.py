from argControll import Arguments
from xmlParse import XMLParser
from structures import *
import os
import sys

def main():
    # kontrola parametrov programu
    argChecker = Arguments()
    argChecker.argCheck()

    # xml parsing
    xmlParsing = XMLParser(argChecker.sourceFlag, argChecker.source)
    instructions = xmlParsing.xmlParse()
    
    # zoznam innstrukci je prazdny -> program ma len hlavičku
    if(len(instructions.instructions) == 0):
        sys.exit(0)

    # v zozname je aspon jedna instrukcia -> ideme v cykle
    variable = Variables()
    stack = Stack()
    callReturnStack = CallReturnStack()
    actualInstruction = 1
    while True:
        instruction = instructions.getNextInstr(actualInstruction)
        if(instruction is None):
            break
        if(instruction.opcode == 'DEFVAR'):
            variable.defvar(instruction.arg1)
        elif(instruction.opcode == 'WRITE'):
            arg_type, arg_value = variable.getTypeAndValue(instruction.arg1)
            if(arg_value is None):
                sys.stderr.write("Pokus o vypis obsahu premennej bez hodnoty: {}\n".format(instruction.arg1.text))
                sys.exit(56)
            elif(arg_type == 'nil'):
                print('')
            else:
                print(arg_value)
        elif(instruction.opcode == 'PUSHS'):
            arg_type, arg_value = variable.getTypeAndValue(instruction.arg1)
            stack.pushStack(arg_type,arg_value)
        elif(instruction.opcode == 'POPS'):
            arg_type, arg_value = stack.popStack()
            variable.setTypeAndValue(instruction.arg1, arg_type, arg_value)
        elif(instruction.opcode == 'ADD'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if arg_type2 == arg_type3:
                if arg_type2 == 'int':
                    value = int(arg_value2) + int(arg_value3)
                    variable.setTypeAndValue(instruction.arg1, 'int', value)
                else:
                    sys.stderr.write("Zly typ operandov pri instrukci ADD - musia byť int\n")
                    sys.exit(53)
            else:
                sys.stderr.write("Zly typ operandov pri instrukci ADD - operandy musia mat rovnake typy INT\n")
                sys.exit(53)
        elif(instruction.opcode == 'SUB'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if arg_type2 == arg_type3:
                if arg_type2 == 'int':
                    value = int(arg_value2) - int(arg_value3)
                    variable.setTypeAndValue(instruction.arg1, 'int', value)
                else:
                    sys.stderr.write("Zly typ operandov pri instrukci SUB - musia byť int\n")
                    sys.exit(53)
            else:
                sys.stderr.write("Zly typ operandov pri instrukci SUB - operandy musia mat rovnake typy INT\n")
                sys.exit(53)
        elif(instruction.opcode == 'MUL'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if arg_type2 == arg_type3:
                if arg_type2 == 'int':
                    value = int(arg_value2) * int(arg_value3)
                    variable.setTypeAndValue(instruction.arg1, 'int', value)
                else:
                    sys.stderr.write("Zly typ operandov pri instrukci MUL - musia byť int\n")
                    sys.exit(53)
            else:
                sys.stderr.write("Zly typ operandov pri instrukci MUL - operandy musia mat rovnake typy INT\n")
                sys.exit(53)
        elif(instruction.opcode == 'IDIV'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if arg_type2 == arg_type3:
                if arg_type2 == 'int':
                    if(int(arg_value3) == 0):
                        sys.stderr.write("Delenie nulou.\n")
                        sys.exit(57)
                    else:
                        value = int(arg_value2) // int(arg_value3)
                        variable.setTypeAndValue(instruction.arg1, 'int', value)
                else:
                    sys.stderr.write("Zly typ operandov pri instrukci IDIV - musia byť int\n")
                    sys.exit(53)
            else:
                sys.stderr.write("Zly typ operandov pri instrukci IDIV - operandy musia mat rovnake typy INT\n")
                sys.exit(53)
        elif(instruction.opcode == 'LT'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if(arg_type2 != arg_type3):
                sys.stderr.write("Zly typ operandov pri instrukci LT - operandy musia mat rovnake typy\n")
                sys.exit(53)
            else:
                if(arg_type2 == 'int'):
                    if(int(arg_value2) < int(arg_value3)):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
                elif(arg_type2 == 'bool'):
                    if(arg_value2 == 'false' and arg_value3 == 'true'):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
                elif(arg_type2 == 'string'):
                    if(arg_value2 < arg_value3):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
                else:
                    sys.stderr.write("Zly typ operandov pri instrukci LT - operandy možu byt intr, bool, string\n")
                    sys.exit(53)
        elif(instruction.opcode == 'GT'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if(arg_type2 != arg_type3):
                sys.stderr.write("Zly typ operandov pri instrukci GT - operandy musia mat rovnake typy\n")
                sys.exit(53)
            else:
                if(arg_type2 == 'int'):
                    if(int(arg_value2) > int(arg_value3)):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
                elif(arg_type2 == 'bool'):
                    if(arg_value2 == 'true' and arg_value3 == 'false'):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
                elif(arg_type2 == 'string'):
                    if(arg_value2 > arg_value3):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
                else:
                    sys.stderr.write("Zly typ operandov pri instrukci GT - operandy možu byt intr, bool, string\n")
                    sys.exit(53)
        elif(instruction.opcode == 'EQ'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if(arg_type2 != 'nil' and arg_type3 != 'nil'):
                if(arg_type2 != arg_type3):
                    sys.stderr.write("Zly typ operandov pri instrukci EQ - operandy musia mat rovnake typy\n")
                    sys.exit(53)
                else:
                    if(arg_value2 == arg_value3):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
            else:
                # porovnavanie s nilom je true len ked oba su nil
                if(arg_type2 == arg_type3):
                    if(arg_value2 == arg_value3):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
                else:
                    variable.setTypeAndValue(instruction.arg1, 'bool', 'false')
        elif(instruction.opcode == 'MOVE'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            variable.setTypeAndValue(instruction.arg1, arg_type2, arg_value2)
            # mozem movnut neinicializovanu premennu do inej ? 
        elif(instruction.opcode == 'AND'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if(arg_type2 != arg_type3):
                sys.stderr.write("Zly typ operandov pri instrukci AND - operandy musia mat rovnake typy\n")
                sys.exit(53)
            else:
                if(arg_type2 != 'bool'):
                    sys.stderr.write("Zly typ operandov pri instrukci AND - operandy musia byt typu bool\n")
                    sys.exit(53)
                else:
                    if(arg_value2 == arg_value3 == 'true'):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
        elif(instruction.opcode == 'OR'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if(arg_type2 != arg_type3):
                sys.stderr.write("Zly typ operandov pri instrukci OR - operandy musia mat rovnake typy\n")
                sys.exit(53)
            else:
                if(arg_type2 != 'bool'):
                    sys.stderr.write("Zly typ operandov pri instrukci OR - operandy musia byt typu bool\n")
                    sys.exit(53)
                else:
                    if(arg_value2 == 'true' or arg_value3 == 'true'):
                        value = 'true'
                    else:
                        value = 'false'
                    variable.setTypeAndValue(instruction.arg1, 'bool', value)
        elif(instruction.opcode == 'NOT'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            if(arg_type2 != 'bool'):
                sys.stderr.write("Zly typ operandu pri instrukci NOT - operand musi byt typu bool\n")
                sys.exit(53)
            else:
                if(arg_value2 == 'true'):
                    value = 'false'
                else:
                    value = 'true'
                variable.setTypeAndValue(instruction.arg1, 'bool', value)
        elif(instruction.opcode == 'INT2CHAR'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            if(arg_type2 != 'int'):
                sys.stderr.write("Zly typ operandu pri instrukci INT2CHAR - operand musi byt typu int\n")
                sys.exit(53)
            else:
                try:
                    value = chr(int(arg_value2))
                except:
                    sys.stderr.write("Nevalidna ordinalna hodnota pri instrukci INT2CHAR\n")
                    sys.exit(58)
                variable.setTypeAndValue(instruction.arg1, 'string', value)
        elif(instruction.opcode == 'STRI2INT'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if(arg_type2 == 'string' and arg_type3 == 'int'):
                try:
                    value = arg_value2[int(arg_value3)]
                    value = ord(value)
                except:
                    sys.stderr.write("Indexacia mimo retazec pri instrukci STRI2INT\n")
                    sys.exit(58)
                variable.setTypeAndValue(instruction.arg1, 'int', value)
            else:
                sys.stderr.write("Zly typ operandov pri instrukci STRI2INT - operandy musia byt typu string a int\n")
                sys.exit(53)
        elif(instruction.opcode == 'CONCAT'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if(arg_type2 != arg_type3):
                sys.stderr.write("Zly typ operandov pri instrukci CONCAT - operandy musia byt typu string\n")
                sys.exit(53)
            else:
                if(arg_type2 != 'string'):
                    sys.stderr.write("Zly typ operandov pri instrukci CONCAT - operandy musia byt typu string\n")
                    sys.exit(53)
                else:
                    value = arg_value2 + arg_value3
                    variable.setTypeAndValue(instruction.arg1, 'string', value)
        elif(instruction.opcode == 'STRLEN'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            if(arg_type2 != 'string'):
                sys.stderr.write("Zly typ operandu pri instrukci STRLEN - operand musi byt typu string\n")
                sys.exit(53)
            else:
                value = len(arg_value2)
                variable.setTypeAndValue(instruction.arg1, 'int', value)
        elif(instruction.opcode == 'GETCHAR'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if(arg_type2 == 'string' and arg_type3 == 'int'):
                try:
                    value = arg_value2[int(arg_value3)]
                except:
                    sys.stderr.write("Indexacia mimo retazec pri instrukci GETCHAR\n")
                    sys.exit(58)
                variable.setTypeAndValue(instruction.arg1, 'string', value)
            else:
                sys.stderr.write("Zly typ operandov pri instrukci GETCHAR - operandy musia byt typu string a int\n")
                sys.exit(53)
        elif(instruction.opcode == 'SETCHAR'):
            arg_type1, arg_value1 = variable.getTypeAndValue(instruction.arg1)
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            if(arg_type1 == 'string' and arg_type2 == 'int' and arg_type3 == 'string'):
                try:
                    arg_value1 = list(arg_value1)
                    arg_value1[int(arg_value2)] = arg_value3[0]
                    arg_value1 = ''.join(arg_value1)
                except:
                    sys.stderr.write("Indexacia mimo retazec pri instrukci SETCHAR alebo prazdny retazec v symb2\n")
                    sys.exit(58)
                variable.setTypeAndValue(instruction.arg1, 'string', arg_value1)
            else:
                sys.stderr.write("Zly typ operandov pri instrukci SETCHAR - operandy musia byt typu int a string a premena musi byt typu string\n")
                sys.exit(53)
        elif(instruction.opcode == 'TYPE'):
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            if arg_type2 is None:
                value = ''
            else:
                value = arg_type2
            variable.setTypeAndValue(instruction.arg1, 'string', value)
        elif(instruction.opcode == 'DPRINT'):
            arg_type1, arg_value1 = variable.getTypeAndValue(instruction.arg1)
            print(arg_value1, file=sys.stderr)
        elif(instruction.opcode == 'EXIT'):
            arg_type1, arg_value1 = variable.getTypeAndValue(instruction.arg1)
            if(arg_type1 != 'int'):
                sys.stderr.write("Zly typ operandu pri instrukci EXIT - operandy musi byt typu int.\n")
                sys.exit(53)
            else:
                value = int(arg_value1)
                if(value >= 0 and value <= 49):
                    sys.exit(value)
                else:
                    sys.stderr.write("EXIT musi byt celociselna hodnota medzi 0 a 49.\n")
                    sys.exit(57)
        elif(instruction.opcode == 'LABEL'):
            actualInstruction += 1
            continue
        elif(instruction.opcode == 'JUMP'):
            arg_type1, arg_value1 = variable.getTypeAndValue(instruction.arg1)
            number = instructions.getLabelCode(arg_value1)
            if(int(number) == -1):
                sys.stderr.write("JUMP na nedefinovany label\n")
                sys.exit(52)
            else:
                actualInstruction = int(number)
        elif(instruction.opcode == 'JUMPIFEQ'):
            arg_type1, arg_value1 = variable.getTypeAndValue(instruction.arg1)
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            # malo by zahrnovat aj nil porovanie
            if(arg_type2 == arg_type3):
                if(arg_value2 == arg_value3):
                    number = instructions.getLabelCode(arg_value1)
                    if(int(number) == -1):
                        sys.stderr.write("JUMP na nedefinovany label\n")
                        sys.exit(52)
                    else:
                        actualInstruction = int(number)
                else:
                    pass
            else:
                sys.stderr.write("Zly typ operandov pri instrukci JUMPIFEQ - operandy musia byt rovnakeho typu.\n")
                sys.exit(53)
        elif(instruction.opcode == 'JUMPIFNEQ'):
            arg_type1, arg_value1 = variable.getTypeAndValue(instruction.arg1)
            arg_type2, arg_value2 = variable.getTypeAndValue(instruction.arg2)
            arg_type3, arg_value3 = variable.getTypeAndValue(instruction.arg3)
            # malo by zahrnovat aj nil porovanie
            if(arg_type2 == arg_type3):
                if(arg_value2 != arg_value3):
                    number = instructions.getLabelCode(arg_value1)
                    if(int(number) == -1):
                        sys.stderr.write("JUMP na nedefinovany label\n")
                        sys.exit(52)
                    else:
                        actualInstruction = int(number)
                else:
                    pass
            else:
                sys.stderr.write("Zly typ operandov pri instrukci JUMPIFEQ - operandy musia byt rovnakeho typu.\n")
                sys.exit(53)
        elif(instruction.opcode == 'CALL'):
            arg_type1, arg_value1 = variable.getTypeAndValue(instruction.arg1)
            callReturnStack.pushStack(actualInstruction + 1)
            
            number = instructions.getLabelCode(arg_value1)
            if(int(number) == -1):
                sys.stderr.write("CALL na nedefinovany label\n")
                sys.exit(52)
            else:
                actualInstruction = int(number)
        elif(instruction.opcode == 'RETURN'):
            actualInstruction = callReturnStack.popStack()
            continue

        actualInstruction += 1
        
        
    
if __name__ == "__main__":
    main()