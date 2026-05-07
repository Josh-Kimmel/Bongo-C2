import requests
from src.serverSettings import *

def getPostByID(id):
    url = getUrl("/api/paste/" + id)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def getUrl(path):
    base = str(getSettings()["stikked_address"]).rstrip("/")
    return base + "/" + path.lstrip("/")

def getReplyIDs(listener_name):
    """Use /api/recent to find reply pastes by matching the RE: <name> title convention."""
    url = getUrl("/api/recent")
    response = requests.get(url)
    response.raise_for_status()
    pastes = response.json()
    expected_title = "RE: " + listener_name
    return [p["pid"] for p in pastes if p.get("title") == expected_title]

def replyPost(content, title, reply_to_pid, expire=None):
    url = getUrl("/api/create")
    payload = {
        "name": getSettingByName("server_username"),
        "title": title,
        "text": str(content),
        "reply": str(reply_to_pid),
    }
    if expire is not None:
        payload["expire"] = str(expire)
    return requests.post(url, data=payload)

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