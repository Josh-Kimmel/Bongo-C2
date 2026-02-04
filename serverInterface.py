import os

def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

def homeScreen():

    homeText = """
    
    #--------# Bongo #--------#
    |                         |
    | [0] - Initialize Server |
    | [1] - Create Listener   |
    | [2] - Send Commands     |
    | [3] - Exit              |
    |                         |
    #-------------------------#

    """

    print(homeText)

def splashScreen():
    pass