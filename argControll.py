import sys

class Arguments:
    """Objekt ktory sa stara o kontrolu parametrov skriptu"""
    def __init__(self):
        self.source = ''
        self.input = ''
        self.sourceFlag = False
        self.inputFlag = False

    def argCheck(self):
        """Metóda pre kontrolu parametrov"""
        if("--help" in sys.argv):
            if(len(sys.argv) == 2):
                self.printHelp()
            else:
               sys.stderr.write("--help sa nemoze kombinovat s inym parametrom\n")
               sys.exit(10) 

        # kontrola ostatnych parametrov --source a --input
        arguments = sys.argv[1:]
        
        for argument in arguments:
            if("--source=" in argument):
                if(self.sourceFlag == True):
                    sys.stderr.write("viacnasobny vyskyt parametra --source\n")
                    sys.exit(10)
                else:
                    self.sourceFlag = True
                    split = argument.split('=', 1)
                    self.source = split[1]

            elif("--input=" in argument):
                if(self.inputFlag == True):
                    sys.stderr.write("viacnasobny vyskyt parametra --input\n")
                    sys.exit(10)
                else:
                    self.inputFlag = True
                    split = argument.split('=', 1)
                    self.input = split[1]
            
            else:
                sys.stderr.write("vyskyt invalidneho parametra\n")
                sys.exit(10)

        if(self.inputFlag == False and self.sourceFlag == False):
            sys.stderr.write("Aspon jeden subor musi byt zadany: source || input\n")
            sys.exit(10)


    def printHelp(self):
        """Metoda pre vypis napovedy a ukoncenie programu"""
        print("Interpret pre IPPcode21 pisany v pythone.\nSkript je spustitelný s nasledujucimi parametrami:\n--help : pre výpis napovedy\n--input=file : subor so vstupmi pre samotnu interpretaciu zadaneho zdrojoveho kodu\n--source=file : vstupný subor s XML reprezentaciou zdrojoveho kodu\nSkript musi byt spusteny aspon s jednym z poslednych dvoch spominanych parametrov.")
        sys.exit(0)


    