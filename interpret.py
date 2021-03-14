from argControll import Arguments

def main():
    # kontrola parametrov programu
    argChecker = Arguments()
    argChecker.argCheck()
    if(argChecker.inputFlag):
        print(argChecker.input)
    else:
        print("source je stdin")

if __name__ == "__main__":
    main()