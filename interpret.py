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
        
        actualInstruction += 1
        
    
if __name__ == "__main__":
    main()