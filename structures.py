import sys

class Instruction:
    """Objekt (struktura bez metód, správa sa ako typedef v C) ktory drzi info o 
    instrukci"""
    def __init__(self, opcode,arg1=None, arg2=None, arg3=None):
        self.opcode = opcode
        if arg1 is not None:
            self.arg1 = arg1
        if arg2 is not None:
            self.arg2 = arg2
        if arg3 is not None:
            self.arg3 = arg3

class InstrDict:
    """Objekt (slovnik instrukci) - zoznam vsetkych instrukci programu"""
    def __init__(self):
        self.instructions = {}
        self.count = 0
        self.labels = {}

    def addInstrToDict(self, instr, position):
        """Pridanie instrukcie do slovnika"""
        self.count += 1
        self.instructions[position] = instr
    
    def addLabel(self, label, order):
        """Pridanie labelu do pola labelov (sluzi pre zistenie duplicity mien)"""
        self.labels[label] = order

    def getNextInstr(self, order):
        """Vrati instrukciu ktora sa bude vykonavat"""
        if(order > self.count):
            return None
        else:
            return self.instructions[order]

    def getLabelCode(self, label):
        """Vrati opcode labelu, pokial neexistuje vrati -1"""
        if label in self.labels:
            return self.labels[label]
        else:
            return -1

class Variables:
    """Objekt ktorý sa stara o pracu s framemami a o pracu s premennymi"""
    def __init__(self):
        self.globalFrame = {}
        self.stack = []
        self.temporaryFrame = {}
        self.accesible = False

    def defvar(self, variable):
        """Funkcia pre definiciu premennej"""
        frame, name = variable.text.split('@', 1)
        if(frame == 'GF'):
            if(name in self.globalFrame):
                sys.stderr.write("Redefinicia premennej s nazvom: {}\n".format(name))
                sys.exit(52)
            else:
                variable = Var()
                self.globalFrame[name] = variable
        elif(frame == 'LF'):
            if(len(self.stack) <= 0):
                sys.stderr.write("Vytvorenie premenej na nedefinovanom ramci.\n")
                sys.exit(55)
            else:
                if(name in self.stack[len(self.stack) - 1]):
                    sys.stderr.write("Redefinicia premennej s nazvom: {}\n".format(name))
                    sys.exit(52)
                else:
                    variable = Var()
                    frame = self.stack[len(self.stack) - 1]
                    frame[name] = variable
        else:
            if self.accesible == False:
                sys.stderr.write("Vytvorenie premenej na nedefinovanom ramci.\n")
                sys.exit(55)
            else:
                if(name in self.temporaryFrame):
                    sys.stderr.write("Redefinicia premennej s nazvom: {}\n".format(name))
                    sys.exit(52)
                else:
                    variable = Var()
                    self.temporaryFrame[name] = variable

    def getTypeAndValue(self, arg):
        """Funkcia ktora vrati typ a hodnotu premennej"""
        if(arg.attrib['type'] == 'var'):
            frame, name = arg.text.split('@', 1)
            if(frame == 'GF'):
                if name not in self.globalFrame:
                    sys.stderr.write("Pristup k neexistujucej premennej: {}\n".format(name))
                    sys.exit(54)
                else:
                    return(self.globalFrame[name].type, self.globalFrame[name].value)
            elif(frame == 'LF'):
                if(len(self.stack) <= 0):
                    sys.stderr.write("Neexistujuci ramec.\n")
                    sys.exit(55)
                else:
                    if(name not in self.stack[len(self.stack) - 1]):
                        sys.stderr.write("Pristup k neexistujucej premennej: {}\n".format(name))
                        sys.exit(54)
                    else:
                        frame = self.stack[len(self.stack) - 1]
                        return(frame[name].type, frame[name].value)
            else:
                if self.accesible == False:
                    sys.stderr.write("Vytvorenie premenej na nedefinovanom ramci.\n")
                    sys.exit(55)
                else:
                    if(name not in self.temporaryFrame):
                        sys.stderr.write("Pristup k neexistujucej premennej: {}\n".format(name))
                        sys.exit(54)
                    else:
                        return(self.temporaryFrame[name].type, self.temporaryFrame[name].value)
        else:
            return(arg.attrib['type'], arg.text)

    def setTypeAndValue(self, var, typ, value):
        """Funkcia ktora nastavi hodnotu a typ premennej"""
        frame, name = var.text.split('@', 1)
        if(frame == 'GF'):
            if name not in self.globalFrame:
                sys.stderr.write("Pristup k neexistujucej premennej: {}\n".format(name))
                sys.exit(54)
            else:
                self.globalFrame[name].type = typ
                self.globalFrame[name].value = value
        elif(frame == 'LF'):
            if(len(self.stack) <= 0):
                sys.stderr.write("Neexistujuci ramec.\n")
                sys.exit(55)
            else:
                if(name not in self.stack[len(self.stack) - 1]):
                    sys.stderr.write("Pristup k neexistujucej premennej: {}\n".format(name))
                    sys.exit(54)
                else:
                    frame = self.stack[len(self.stack) - 1]
                    frame[name].type = typ
                    frame[name].value = value
        else:
            if self.accesible == False:
                sys.stderr.write("Vytvorenie premenej na nedefinovanom ramci.\n")
                sys.exit(55)
            else:
                if(name not in self.temporaryFrame):
                    sys.stderr.write("Pristup k neexistujucej premennej: {}\n".format(name))
                    sys.exit(54)
                else:
                    self.temporaryFrame[name].type = typ
                    self.temporaryFrame[name].value = value
                    
    
    def createTF(self):
        """Vytvorenie Temporary framu"""
        self.temporaryFrame = {}
        self.accesible = True
    
    def pushTF(self):
        """Pridanie temporary framu na vrchol zasobnika"""
        if(self.accesible == False):
            sys.stderr.write("Pristup k nedefinovanemu ramcu.\n")
            sys.exit(55)
        else:
            self.stack.append(self.temporaryFrame)
            self.accesible = False
    
    def popTF(self):
        """Odobratie framu zo zasobnika a priradenie do temporary framu"""
        if(len(self.stack) <= 0):
            sys.stderr.write("Ziadny ramec v LF neni k dispozici.\n")
            sys.exit(55)
        else:
            self.temporaryFrame = self.stack.pop()
            self.accesible = True

class Var:
    """Objekt (struktura) pre premennu"""
    def __init__(self):
        self.type = None
        self.value = None

    def setValue(self, value):
        """Setter hodnoty"""
        self.value = value

    def setType(self, typ):
        """Setter typu"""
        self.type = typ

class Stack:
    """Zasobnik pre pushs a pops"""
    def __init__(self):
        self.stack = []

    def pushStack(self, typ, value):
        """Vlozi hodnotu a typ do zasobnika"""
        self.stack.append((typ, value))

    def popStack(self):
        """Vyberie hodnotu a typ zo zasobnika"""
        if(len(self.stack) <= 0):
            sys.stderr.write("Chybajuca hodnotu v datovom zasobniku-\n")
            sys.exit(56)
        else:
            return self.stack.pop()

class CallReturnStack:
    """Zasobnik pre call a reuturn hodnoty"""
    def __init__(self):
        self.stack = []

    def pushStack(self, value):
        """Vlozi poziciu instrukcie za instrukciou CALL do zasobnika"""
        self.stack.append(value)

    def popStack(self):
        """Vyberie poziciu zo zasobnika"""
        if(len(self.stack) <= 0):
            sys.stderr.write("Chybajuca hodnotu v datovom zasobniku-\n")
            sys.exit(56)
        else:
            return self.stack.pop()