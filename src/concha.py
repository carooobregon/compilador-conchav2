from driver import Driver
from pathlib import Path

def inputUser():
    data_folder = Path("tests/")
    arch = input()
    file_to_open = data_folder / arch
    file = open(str(file_to_open), "r")
    user_input = file.read()
    return user_input

def main():
    conchaDriver = Driver()
    correct_test = inputUser()
    conchaDriver.compileAndRun(correct_test)

if __name__=='__main__':
    main()# Stack example