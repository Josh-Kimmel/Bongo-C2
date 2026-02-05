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
    #get file content

    fileContent = ""
    try:
        with open(filePath, "rt") as file:
            fileContent = file.read()
    except:
        print("An error was encountered attempting to read " + filePath)

    #send file
    response = makePost(fileContent)

    #save file info
    if(response.status_code != 200):
        print("error")
    else:
        fileInfo = {
            "name": fileName,
            "url": response.text[:-1],
            "id": response.text [-9:-1],
            "comment": fileComment
        }
    


def saveFileInformation(fileInfo):
    config = readConfig()
    config["files"].append(fileInfo)
