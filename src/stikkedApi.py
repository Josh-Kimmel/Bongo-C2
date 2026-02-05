import requests
from src.serverSettings import *

def getPostByID(id):
    url = getUrl("/api/paste/" + id)
    
    return requests.get(url)

def getUrl(path):
    stikked_address = getSettings()["stikked_address"]
    
    return stikked_address + path

def makePost(content):
    url = getUrl("/api/create")
    payload = {
        "private": 1,
        "name": getSettingByName("server_username"), 
        "text": str(content), 
        "expire": 5
    }
   
    return requests.post(url, payload)