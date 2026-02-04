#! /bin/python3
import json

#reads in json server config file
def readSettings(configFileName):
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
def writeSettings(configFileName, configJson):
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
    serverConfigFile = "serverConfig.json"

    print("Initializing server.\n")
    configJson = readSettings(serverConfigFile)
    newConfigJson = _initSettings(configJson)
    writeSettings(serverConfigFile, newConfigJson)
