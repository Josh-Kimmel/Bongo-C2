from src.serverSettings import *
from src.serverInterface import *

def load():

    splashScreen()
    
    config = readConfig()
    if(not config["server_data"]["initialized"]):
        initialize()

def home():

    homeScreen()
    selection = input("Option: ")
    clearScreen()
    
    match selection:
        case "0":
            initialize()
            home()

        case "1":
            #viewSettings()
            home()
        
        case "2":
            #viewSessions()
            home()

        case "3":
            #createListener
            home()

        case "4":
            #sendCommands
            home()

        case "5":
            pass
            home()

        case "6":
            exit

        case _:
            home()