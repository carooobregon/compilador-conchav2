from driver import Driver
from pathlib import Path

# Receives the file name that user wants to compile
def inputUser():
    data_folder = Path("tests/")
    arch = "arreglos.txt"
    file_to_open = data_folder / arch
    file = open(str(file_to_open), "r")
    user_input = file.read()
    return user_input

# Main function of the compiler, running this main lets you compile and run any file written in concha
def main():
    conchaDriver = Driver()
    correct_test = inputUser()
    conchaDriver.compileAndRun(correct_test)

if __name__=='__main__':
    main()# Stack example