#! /bin/python3
from dotenv import load_dotenv
import json
import os

#reads in json server config file
def readConfig():
    load_dotenv()
    configFileName = os.getenv("serverConfigFile")
    
    try:
        with open(configFileName, mode = "rt") as configFile:
            configJson = json.load(configFile)
            configFile.close()
        return configJson


    except FileNotFoundError:
        print("Error: File " + configFileName + " was not found.")
        exit
    except PermissionError:
        print("Error: Permissions denied for file " + configFileName + ".")
    except:
        print("Error: Unknown error in reading file " + configFileName + ".")
        exit


#sets server configuration values
def _initSettings(configJson):
    try:
        
        configJson["server_data"]["initialized"] = True

        ##                                       ##
        # - Add settings to be initialized here - #
        ##                                       ##

        configJson["server_data"]["stikked_address"] = input(
            "\nEnter full URI to stikked server (Example: https://example.com/stikked): "
        )

        configJson["server_data"]["server_username"] = input(
            "\nEnter username for this server to use in stikked posts: "
        )

        ##                                       ##
        # --------------------------------------- #
        ##                                       ##
        
        return configJson

    except json.JSONDecodeError: 
        print("Error: Failed to decode json from serverConfig.json.")
        exit
    except:
        print("Error: Unknown error in initializing server settings.")
        exit

#writes initialized values back to json server config file
def writeConfig(configJson):
    load_dotenv()
    configFileName = os.getenv("serverConfigFile")
    
    try:
        with open(configFileName, "wt") as configFile:

            json.dump(configJson, configFile)
            configFile.close()
        

    except FileNotFoundError:
        print("Error: File " + configFileName + " was not found.")
        exit
    except PermissionError:
        print("Error: Permissions denied for file " + configFileName + ".")
    except:
        print("Error: Unknown error in reading file " + configFileName + ".")
        exit



def initialize():
    print("Initializing server.\n")
    configJson = readConfig()
    newConfigJson = _initSettings(configJson)
    writeConfig(newConfigJson)
