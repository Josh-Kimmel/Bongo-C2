from src.serverSettings import *
from src.listeners import *
from src.serverInterface import *

def getSettingByName(targetName):
    settingsList = getSettings()
    return settingsList[targetName]

def getSettings():
    settingsList = readConfig()["server_data"]
    return settingsList

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
            #viewFiles()
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


def viewSettings():
    settingsList = getSettings()

    for setting in settingsList.keys():
        print(setting + " : " + str(settingsList[setting]))

    print("\n\n")
    waitToContinue()
    clearScreen()

def viewListeners():
    listenersList = getListeners()

    displayList(listenersList)
    waitToContinue()
    clearScreen()


def waitToContinue():
    input("Press [Enter] to continue:")