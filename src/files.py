from src.serverSettings import *
from src.stikkedApi import *

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

def postFile():
    filePath = input("\nEnter path to file to post: ")
    fileName = input("\nEnter name of file to post: ")
    fileComment = input("\nEnter comment on file to post: ")

    fileContent = ""
    try:
        with open(filePath, "rt") as file:
            fileContent = file.read()
    except:
        print("Error: Failed to read " + filePath)

    try:
        response = makePost(fileContent)
    except:
        print("Error: Unable to connect to Stikked server.")
    
    try:
        if(response.status_code != 200):
            print("Error: Unsucessful POST request.")
        else:
            fileInfo = {
                "name": fileName,
                "url": response.text[:-1],
                "id": response.text [-9:-1],
                "comment": fileComment
            }
            saveFileInformation(fileInfo)
    except:
        print("Error: Unable to process response.")
    
    
    


def saveFileInformation(fileInfo):
    config = readConfig()
    config["files"].append(fileInfo)
