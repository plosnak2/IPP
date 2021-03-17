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
    actualInstruction = 1
    while True:
        instruction = instructions.getNextInstr(actualInstruction)
        if(instruction is None):
            break
        if(instruction.opcode == 'DEFVAR'):
            variable.defvar(instruction.arg1)
        elif(instruction.opcode == 'PRINT'):
            pass
        
        actualInstruction += 1
        
    
if __name__ == "__main__":
    main()