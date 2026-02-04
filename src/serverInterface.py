import os

def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

def homeScreen():

    homeText = """
    
    #--------# Bongo #--------#
    |                         |
    | [0] - Initialize Server |
    | [1] - View Settings     |
    | [2] - View Sessions     |
    | [3] - Create Listener   |
    | [4] - Send Commands     |
    | [5] - Delete Sessions   |
    | [6] - Exit              |
    |                         |
    #-------------------------#

    """

    print(homeText)

def splashScreen():
    
    splashText = """

 ----------------------------------------------------

   $$$$$$$\                                          
   $$  __$$\                                         
   $$ |  $$ | $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  
   $$$$$$$\ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
   $$  __$$\ $$ /  $$ |$$ |  $$ |$$ /  $$ |$$ /  $$ |
   $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
   $$$$$$$  |\$$$$$$  |$$ |  $$ |\$$$$$$$ |\$$$$$$  |
   \_______/  \______/ \__|  \__| \____$$ | \______/ 
                                 $$\   $$ |          
                                 \$$$$$$  |          
                                  \______/           

  Asynchronous Command and Control
 ----------------------------------------------------
    """

    print(splashText)