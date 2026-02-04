from serverSettings import *


def load():
    config = readConfig()
    
    if(not config["server_data"]["initialized"]):
        initialize()
