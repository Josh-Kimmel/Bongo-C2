from src.serverSettings import *
from src.stikkedApi import *

def getListenerById(targetId):
    listenerList = getListeners()
    for listener in listenerList:
        if(listener["id"] == targetId):
            return listener
    
    return None


def getListeners():
    listenerList = readConfig()["listeners"]
    return listenerList



def postListener():
    listenerName = input("\nEnter name of the listener: ")
    listenerComment = input("\nEnter comment on listener: ")

    try:
        response = makePost("", listenerName)
    except:
        print("Error: Unable to connect to Stikked server.")

    try:
        if(response.status_code != 200):
            print("Error: Unsucessful POST request.")
        else:
            listenerInfo = {
                "name": listenerName,
                "url": response.text[:-1],
                "id": response.text [-9:-1],
                "comment": listenerComment
            }
            saveListenerInformation(listenerInfo)
    except:
        print("Error: Unable to process response.")

def saveListenerInformation(listenerInfo):
    config = readConfig()
    config["listeners"].append(listenerInfo)




