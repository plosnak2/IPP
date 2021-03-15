from argControll import Arguments
from xmlParse import XMLParser
import os

def main():
    # kontrola parametrov programu
    argChecker = Arguments()
    argChecker.argCheck()

    # xml parsing
    xmlParsing = XMLParser(argChecker.sourceFlag, argChecker.source)
    xmlParsing.xmlParse()
    print("OK")
    
    
if __name__ == "__main__":
    main()