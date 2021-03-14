import os
import sys
import xml.etree.ElementTree as ET

class XMLParser:
    def __init__(self, flag, source):
        self.flag = flag
        if(self.flag):
            self.source = source
        else:
            self.source = sys.stdin

    
    def xmlStruct(self):
        """Funkcia na kontrolu zakladnej struktury XML"""
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
            order = int(instr.attrib['order'])
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
        check = 1
        for i in instr_order:
            if(i != check):
                sys.stderr.write("Zle poradie orderov pri elementoch instrukci\n")
                sys.exit(32)
            check += 1
        # struktura XML suboru skontrolovana

        # kontrola syntaxi a semantiky XML
        # TODO 15.3 SMRCKABAT
        
        
        
