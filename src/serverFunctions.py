from src.serverSettings import *
from src.listeners import *
from src.serverInterface import *
from src.files import *



def home(reminderText=""):

    homeScreen()
    print(reminderText)
    selection = input("Option: ")
    clearScreen()
    
    match selection:
        case "0":
            initialize()
            home()

        case "1":
            viewSettings()
            home()
        
        case "2":
            viewListeners()
            home()

        case "3":
            viewFiles()
            home()

        case "4":
            #createListener
            home()

        case "5":
            #postFile()
            home()

        case "6":
            #sendCommands
            home()

        case "7":
            pass
            home()

        case "8":
            exit

        case _:
            home("Please enter a number selection.")


def load():

    splashScreen()
    
    config = readConfig()
    if(not config["server_data"]["initialized"]):
        initialize()

def viewFiles():
    filesList = getFiles()
    displayList(filesList)
    waitToContinue()
    clearScreen()

def viewListeners():
    listenersList = getListeners()
    displayList(listenersList)
    waitToContinue()
    clearScreen()

def viewSettings():
    settingsDictionary = getSettings()
    displayDictionary(settingsDictionary)
    waitToContinue()
    clearScreen()


def waitToContinue():
    input("Press [Enter] to continue:")