import os

def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

def displayDictionary(dictionary):
    displayList([dictionary])

def displayList(list):
    entries, longestString = _formatList(list)
    
    if(longestString % 2 == 0):
        longestString += 1
    if(longestString < 13):
        longestString = 13

    topSpacing = (int((longestString - 7) / 2)) * "-"
    listText = "   #-" + topSpacing + " Bongo " + topSpacing + "-#\n"
    #listText += "   | " + (longestString * " ") + " |\n"

    for entry in entries:
        if(entry[0:6] == "start"):
            listText += "   | " + (longestString * " ") + " |\n"
        elif(entry[0:3] == "end"):
            listText += "   | " + (longestString * " ") + " |\n"
            listText += "   #-" + (longestString * "-") + "-#\n"
        else:
            spacing = longestString - len(entry)
            listText += "   | " + entry + (spacing * " ") + " |\n"
        
    print(listText)

#formats individual dictionaries for display
def _formatDictionary(dictionary):
    dictionaryEntries = []
    longestString = 0
    
    dictionaryEntries.append("start")

    for key in dictionary:
        entry = key + " : " + str(dictionary[key])
        dictionaryEntries.append(entry)
        
        if(longestString < len(entry)):
            longestString = len(entry)
    
    dictionaryEntries.append("end")
        
    return dictionaryEntries, longestString

#formats lists of dictionaries for display
def _formatList(list):
    entries = []
    longestString = 0

    for dictionary in list:
        currentEntries, currentLongest = _formatDictionary(dictionary)
        entries.extend(currentEntries)

        if(longestString < currentLongest):
            longestString = currentLongest
    
    return entries, longestString


        




def homeScreen():

    homeText = """
    
    #--------# Bongo #--------#
    |                         |
    | [0] - Initialize Server |
    | [1] - View Settings     |
    | [2] - View Listeners    |
    | [3] - View Files        |
    | [4] - Create Listener   |
    | [5] - Post File         |
    | [6] - Send Commands     |
    | [7] - Delete Sessions   |
    | [8] - Exit              |
    |                         |
    #-------------------------#

    """

    print(homeText)

def splashScreen():
    
    splashText = r"""

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