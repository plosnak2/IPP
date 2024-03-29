import os
import sys
import xml.etree.ElementTree as ET
import re
from structures import *

class XMLParser:
    """Objekt ktory sa stara o spracovanie celeho XML"""
    def __init__(self, flag, source):
        self.flag = flag
        if(self.flag):
            self.source = source
        else:
            self.source = sys.stdin

    
    def xmlParse(self):
        """Funkcia na kontrolu zakladnej struktury XML a syntaktickych a lexikalnych chyb v XML"""
        try:
            tree = ET.parse(self.source)
            self.root = tree.getroot()
        except FileNotFoundError:
            sys.stderr.write("Nepodarilo sa otvorit subor\n")
            sys.exit(11)
        except:
            sys.stderr.write("Zla struktura XML\n")
            sys.exit(31)

        # root element musi byť program
        if(self.root.tag != 'program'):
            sys.stderr.write("Root element musi byt program - chybne XML\n")
            sys.exit(32)

        # program musi mat atribut language
        try:
            language = self.root.attrib['language']
        except:
            sys.stderr.write("Program musi mat atribut language\n")
            sys.exit(32)
        
        # language musi byt ippcode21
        language = language.lower()
        if(language != 'ippcode21'):
            sys.stderr.write("Language musi byt ippcode21\n")
            sys.exit(32)
        
        # kontrola jednotlivých inštrukci
        # pole pre kontrolu orderov pri instrukciach
        instr_order = []
        for instr in self.root:
            if(instr.tag != 'instruction'):
                sys.stderr.write("Rodičovske elementy možu byt iba instruction\n")
                sys.exit(32)
            if 'order' not in instr.attrib:
                sys.stderr.write("Element instrukcie nema atribut order\n")
                sys.exit(32)
            if 'opcode' not in instr.attrib:
                sys.stderr.write("Element instrukcie nema atribut opcode\n")
                sys.exit(32)

            try:
                order = int(instr.attrib['order'])
            except:
                sys.stderr.write("Order musi byt číslo\n")
                sys.exit(32)
            if(order in instr_order):
                sys.stderr.write("Duplicitny order pri instrukci\n")
                sys.exit(32)
            if(order <= 0):
                sys.stderr.write("Negativny order pri instrukci\n")
                sys.exit(32)
            
            instr_order.append(order)

            arg_order = 1
            for arg in instr:
                arg_name = "arg" + str(arg_order)
                # kontrola mena elementu
                if(arg.tag != arg_name):
                    sys.stderr.write("Synovske elementy možu byt iba argX kde X je poradie argumentu\n")
                    sys.exit(32)
                # kontrola poctu argumentov elementu
                if(len(arg.attrib) != 1):
                    sys.stderr.write("Arg elementy mozu mat len jeden atribut\n")
                    sys.exit(32)
                # kontrola atributu elementu
                if 'type' not in arg.attrib:
                    sys.stderr.write("Arg elementy musia mat atribut type\n")
                    sys.exit(32)
                # kontrola daneho typu
                arg_type = arg.attrib['type']
                if arg_type not in ['var', 'string', 'label', 'int', 'bool', 'type', 'nil']:
                    sys.stderr.write("Type atribut musi byt len var, string, bool, int, type, label, nil\n")
                    sys.exit(32)
                # zvyšenie premennej ktora modifikuje nazov arg elementu
                arg_order += 1

        # kontrola orderu jednotlivych instrukci -> ordery instrukci musia ist vzostupne od 1
        """
        check = 1
        for i in instr_order:
            if(i != check):
                sys.stderr.write("Zle poradie orderov pri elementoch instrukci\n")
                sys.exit(32)
            check += 1
        """
        sort = sorted(instr_order)
        # struktura XML suboru skontrolovana

        # kontrola syntaxi a semantiky XML
        instructions = InstrDict()
        for instr in self.root:
            index = sort.index(int(instr.attrib['order'])) + 1
            instr.attrib['opcode'] = instr.attrib['opcode'].upper()
            if(instr.attrib['opcode'] == 'MOVE'):
                if(len(list(instr)) == 2):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    instruction = Instruction('MOVE', instr[0], instr[1])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia MOVE ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'CREATEFRAME'):
                if(len(list(instr)) == 0):
                    instruction = Instruction('CREATEFRAME')
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia CREATEFRAME ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'PUSHFRAME'):
                if(len(list(instr)) == 0):
                    instruction = Instruction('PUSHFRAME')
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia PUSHFRAME ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'POPFRAME'):
                if(len(list(instr)) == 0):
                    instruction = Instruction('POPFRAME')
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia POPFRAME ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'DEFVAR'):
                if(len(list(instr)) == 1):
                    self.varSyntax(instr[0])
                    instruction = Instruction('DEFVAR', instr[0])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia DEFVAR ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'CALL'):
                if(len(list(instr)) == 1):
                    self.labelSyntax(instr[0])
                    instruction = Instruction('CALL', instr[0])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia CALL ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'RETURN'):
                if(len(list(instr)) == 0):
                    instruction = Instruction('RETURN')
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia RETURN ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'PUSHS'):
                if(len(list(instr)) == 1):
                    self.symbSyntax(instr[0])
                    instruction = Instruction('PUSHS', instr[0])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia PUSHS ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'POPS'):
                if(len(list(instr)) == 1):
                    self.varSyntax(instr[0])
                    instruction = Instruction('POPS', instr[0])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia POPS ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'ADD'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('ADD', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia ADD ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'SUB'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('SUB', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia SUB ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'MUL'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('MUL', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia MUL ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'IDIV'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('IDIV', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia IDIV ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'LT'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('LT', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia LT ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'GT'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('GT', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia GT ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'EQ'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('EQ', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia EQ ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'AND'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('AND', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia AND ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'OR'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('OR', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia OR ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'NOT'):
                if(len(list(instr)) == 2):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    instruction = Instruction('NOT', instr[0], instr[1])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia NOT ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'INT2CHAR'):
                if(len(list(instr)) == 2):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    instruction = Instruction('INT2CHAR', instr[0], instr[1])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia INT2CHAR ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'STRI2INT'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('STRI2INT', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia STRI2INT ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'READ'):
                if(len(list(instr)) == 2):
                    self.varSyntax(instr[0])
                    self.typeSyntax(instr[1])
                    instruction = Instruction('READ', instr[0], instr[1])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia READ ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'WRITE'):
                if(len(list(instr)) == 1):
                    self.symbSyntax(instr[0])
                    instruction = Instruction('WRITE', instr[0])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia WRITE ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'CONCAT'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('CONCAT', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia CONCAT ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'STRLEN'):
                if(len(list(instr)) == 2):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    instruction = Instruction('STRLEN', instr[0], instr[1])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia STRLEN ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'GETCHAR'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('GETCHAR', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia GETCHAR ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'SETCHAR'):
                if(len(list(instr)) == 3):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('SETCHAR', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia SETCHAR ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'TYPE'):
                if(len(list(instr)) == 2):
                    self.varSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    instruction = Instruction('TYPE', instr[0], instr[1])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia TYPE ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'LABEL'):
                if(len(list(instr)) == 1):
                    self.labelSyntax(instr[0])
                    instruction = Instruction('LABEL', instr[0])
                    instructions.addInstrToDict(instruction, index)
                    if(instr[0].text in instructions.labels):
                        sys.stderr.write("2 labely s rovnakym menom\n")
                        sys.exit(52)
                    else:
                        instructions.addLabel(instr[0].text, index)
                else:
                    sys.stderr.write("Instrukcia LABEL ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'JUMP'):
                if(len(list(instr)) == 1):
                    self.labelSyntax(instr[0])
                    instruction = Instruction('JUMP', instr[0])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia JUMP ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'JUMPIFEQ'):
                if(len(list(instr)) == 3):
                    self.labelSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('JUMPIFEQ', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia JUMPIFEQ ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'JUMPIFNEQ'):
                if(len(list(instr)) == 3):
                    self.labelSyntax(instr[0])
                    self.symbSyntax(instr[1])
                    self.symbSyntax(instr[2])
                    instruction = Instruction('JUMPIFNEQ', instr[0], instr[1], instr[2])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia JUMPIFNEQ ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'EXIT'):
                if(len(list(instr)) == 1):
                    self.symbSyntax(instr[0])
                    instruction = Instruction('EXIT', instr[0])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia EXIT ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'DPRINT'):
                if(len(list(instr)) == 1):
                    self.symbSyntax(instr[0])
                    instruction = Instruction('DPRINT', instr[0])
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia DPRINT ma zly pocet parametrov\n")
                    sys.exit(32)
            elif(instr.attrib['opcode'] == 'BREAK'):
                if(len(list(instr)) == 0):
                    instruction = Instruction('BREAK')
                    instructions.addInstrToDict(instruction, index)
                else:
                    sys.stderr.write("Instrukcia BREAK ma zly pocet parametrov\n")
                    sys.exit(32)
            else:
                sys.stderr.write("Nevalidna instrukcia\n")
                sys.exit(32)
        return instructions

    def typeSyntax(self, arg):
        """Funkcia na skontrolovanie spravnosti typu (podobne ako v parseri)"""
        if(arg.attrib['type'] != 'type'):
            sys.stderr.write("Element arg ma zly type - musi byt type\n")
            sys.exit(32)
        else:
            if(arg.text != 'int' and arg.text != 'bool' and arg.text != 'string'):
                sys.stderr.write("Arg s type type može byt iba string int bool\n")
                sys.exit(32)

    def labelSyntax(self, arg):
        """Funkcia na skontrolovanie spravnosti labelu (podobne ako v parseri)"""
        if(arg.attrib['type'] != 'label'):
            sys.stderr.write("Element arg ma zly type - musi byt label\n")
            sys.exit(32)
        else:
            if not re.match(r'^[a-zA-Z_\-$_&!?%*][a-zA-Z0-9_\-$_!?&%*]*$', arg.text):
                sys.stderr.write("Label obsahuje zle znaky alebo ma zly format\n")
                sys.exit(32)

    def varSyntax(self,arg):
        """Funkcia na skontrolovanie spravnosti var (podobne ako v parseri)"""
        if(arg.attrib['type'] != 'var'):
            sys.stderr.write("Element arg ma zly type - musi byt var\n")
            sys.exit(32)
        else:
            var = arg.text.split('@')
            if(len(var) != 2):
                sys.stderr.write("Zly nazov premennej - musi byt RAMEC@meno\n")
                sys.exit(32)
            if(var[0] != 'LF' and var[0] != 'GF' and var[0] != 'TF'):
                sys.stderr.write("Zly nazov premennej - ramec moze byt TF GF LF\n")
                sys.exit(32)
            if not re.match(r'^[a-zA-Z_\-$_&!?%*][a-zA-Z0-9_\-$_!?&%*]*$',var[1]):
                sys.stderr.write("Var obsahuje zle znaky alebo ma zly format\n")
                sys.exit(32)

    def symbSyntax(self, arg):
        """Funkcia na skontrolovanie spravnosti symbolu (podobne ako v parseri)"""
        if(arg.attrib['type'] == 'var'):
            self.varSyntax(arg)
        elif(arg.attrib['type'] == 'bool'):
            if(arg.text != 'true' and arg.text != 'false'):
                sys.stderr.write("Type bool musi byt true alebo false\n")
                sys.exit(32)
        elif(arg.attrib['type'] == 'int'):
            if not re.match(r'^[+-]?[0-9]+$', arg.text):
                sys.stderr.write("Type int je v zlom formate\n")
                sys.exit(32)
        elif(arg.attrib['type'] == 'string'):
            if arg.text is None:
                arg.text = ''
            else:
                if re.search(r"(?!\\[0-9]{3})[\s\\#]", arg.text):
                    sys.stderr.write("Type string je v zlom formate\n")
                    sys.exit(32)
                # prevod esc sekvencie na char
                arg.text = re.sub(r'\\([0-9]{3})', lambda x: chr(int(x.group(1))), arg.text)
        elif(arg.attrib['type'] == 'nil'):
            if arg.text != 'nil':
                sys.stderr.write("Type nil je v zlom formate\n")
                sys.exit(32)
        else:
            sys.stderr.write("Zly type pri symbole\n")
            sys.exit(32)
            