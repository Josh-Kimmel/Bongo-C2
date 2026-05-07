from src.serverSettings import *
from src.stikkedApi import *

def getListenerById(targetId):
    listenerList = getListeners()
    for listener in listenerList:
        if(listener["id"] == targetId):
            return listener
    return None


def addReplyToListener(listener_id, reply_pid):
    config = readConfig()
    for listener in config["listeners"]:
        if listener["id"] == listener_id:
            if "replies" not in listener:
                listener["replies"] = []
            listener["replies"].append(reply_pid)
            writeConfig(config)
            return


def getListeners():
    listenerList = readConfig()["listeners"]
    return listenerList



def postListener():
    listenerName = input("\nEnter name of the listener: ")
    listenerComment = input("\nEnter comment on listener: ")

    try:
        response = makePost(listenerName, listenerName)
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
            savePostInformation("listeners", listenerInfo)
    except:
        print("Error: Unable to process response.")






