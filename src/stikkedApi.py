import requests
from src.serverSettings import *

def getPostByID(id):
    url = getUrl("/api/paste/" + id)
    
    return requests.get(url)

def getUrl(path):
    stikked_address = getSettings()["stikked_address"]
    
    return stikked_address + path

def makePost(content, title=""):
    url = getUrl("/api/create")
    payload = {
        #"private": 1,
        "name": getSettingByName("server_username"),
        "title": title,
        "text": str(content)
        #"expire": 5 #delete while not testing
    }
    return requests.post(url, payload)