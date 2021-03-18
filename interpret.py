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
        
        actualInstruction += 1
        
    
if __name__ == "__main__":
    main()