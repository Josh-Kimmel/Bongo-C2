from src.serverSettings import *

def getFileById(targetId):
    fileList = getFiles()
    for file in fileList:
        if(file["id"] == targetId):
            return file
    
    return None

def getFileByName(targetName):
    fileList = getFiles()
    for file in fileList:
        if(file["id"] == targetName):
            return file
    
    return None

def getFiles():
    fileList = readConfig()["files"]
    return fileList
