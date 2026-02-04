from src.serverSettings import *


def getListenerById(targetId):
    listenerList = getListeners()
    for listener in listenerList:
        if(listener["id"] == targetId):
            return listener
    
    return None


def getListeners():
    listenerList = readConfig()["listeners"]
    return listenerList



