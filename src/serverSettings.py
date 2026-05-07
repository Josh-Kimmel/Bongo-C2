#! /bin/python3
from dotenv import load_dotenv, find_dotenv
import json
import os

def _fresh_config():
    return {
        "server_data": {
            "initialized": False,
            "stikked_address": "",
            "server_username": "",
        },
        "listeners": [],
        "files": [],
    }

def _config_is_valid(configJson):
    if not isinstance(configJson, dict):
        return False
    sd = configJson.get("server_data")
    if not isinstance(sd, dict):
        return False
    for key in ("initialized", "stikked_address", "server_username"):
        if key not in sd:
            return False
    if not isinstance(configJson.get("listeners"), list):
        return False
    if not isinstance(configJson.get("files"), list):
        return False
    return True

def getSettingByName(targetName):
    settingsList = getSettings()
    return settingsList[targetName]

def getSettings():
    settingsList = readConfig()["server_data"]
    return settingsList

#initializes server settings 
def initialize():
    print("Initializing server.\n")
    configJson = readConfig()
    newConfigJson = _initSettings(configJson)
    writeConfig(newConfigJson)


#sets server configuration values
def _initSettings(configJson):
    try:
        ##                                       ##
        # - Add settings to be initialized here - #
        ##                                       ##

        configJson["server_data"]["stikked_address"] = input(
            "\nEnter full URI to stikked server (Example: https://example.com/stikked): "
        )

        configJson["server_data"]["server_username"] = input(
            "\nEnter username for this server to use in stikked posts: "
        )

        configJson["server_data"]["initialized"] = True

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


#reads in json server config file
def readConfig():
    load_dotenv()
    load_dotenv(find_dotenv(usecwd = True))
    configFileName = os.getenv("serverConfigFile")
    if not configFileName:
        print(
            'Error: serverConfigFile is not set. Add it to .env '
            '(e.g. serverConfigFile="serverConfig.json").'
        )
        raise SystemExit(
            'Error: serverConfigFile is not set. Add it to .env '
            '(e.g. serverConfigFile="serverConfig.json").'
        )

    def reset_and_return(reasonMessage):
        fresh = _fresh_config()
        print(reasonMessage)
        print("Config has been reset; you will be asked to set up the server again.\n")
        try:
            with open(configFileName, "wt") as configFile:
                json.dump(fresh, configFile)
                configFile.close()
        except (FileNotFoundError, PermissionError, TypeError):
            print("Error: Could not write reset config to " + str(configFileName) + ".")
            exit
        return fresh

    try:
        with open(configFileName, mode = "rt") as configFile:
            raw = json.load(configFile)
            configFile.close()

        if not _config_is_valid(raw):
            return reset_and_return(
                "serverConfig.json is missing required fields or is not a valid config object."
            )
        return raw

    except FileNotFoundError:
        return reset_and_return(
            "Config file " + str(configFileName) + " was not found; creating a new one."
        )
    except json.JSONDecodeError:
        return reset_and_return("serverConfig.json is not valid JSON.")
    except PermissionError:
        print("Error: Permissions denied for file " + configFileName + ".")
        exit
    except:
        print("Error: Unknown error in reading file " + configFileName + ".")
        exit

def savePostInformation(list, postInfo):
    config = readConfig()
    config[list].append(postInfo)
    writeConfig(config)

#writes initialized values back to json server config file
def writeConfig(configJson):
    load_dotenv()
    load_dotenv(find_dotenv(usecwd = True))
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



