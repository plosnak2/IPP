import sys

class Instruction:
    def __init__(self, opcode,arg1=None, arg2=None, arg3=None):
        self.opcode = opcode
        if arg1 is not None:
            self.arg1 = arg1
        if arg2 is not None:
            self.arg2 = arg2
        if arg3 is not None:
            self.arg3 = arg3

class InstrDict:
    def __init__(self):
        self.instructions = {}
        self.count = 0
        self.labels = {}

    def addInstrToDict(self, instr):
        self.count += 1
        self.instructions[self.count] = instr
    
    def addLabel(self, label, order):
        self.labels[label] = order

    def getNextInstr(self, order):
        if(order > self.count):
            return None
        else:
            return self.instructions[order]

class Variables:
    def __init__(self):
        self.globalFrame = {}

    def defvar(self, variable):
        frame, name = variable.text.split('@', 1)
        if(frame == 'GF'):
            if(name in self.globalFrame):
                sys.stderr.write("Redefinicia premennej s nazvom: {}\n".format(name))
                sys.exit(52)
            else:
                variable = Var()
                self.globalFrame[name] = variable

class Var:
    def __init__(self):
        self.type = None
        self.value = None

    def setValue(self, value):
        self.value = value

    def setType(self, typ):
        self.type = typ
