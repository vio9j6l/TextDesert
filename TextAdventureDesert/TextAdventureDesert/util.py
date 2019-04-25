import sys
from time import sleep


def printGameText(x):
    #print(x)
    for character in x:
        sys.stdout.write(character)
        sys.stdout.flush()
        #print(character, end = '')
        #time.sleep(.035)
        sleep(.005)


def pause():
    input("Press any key to continue...")


def getIntInput(sInput):

    while True:

        try:
            itemChoice = int(input(sInput))
        except ValueError: #Catch exception if input isn't int
            print("\nInvalid item choice")
            continue#Restart loop
        return itemChoice
