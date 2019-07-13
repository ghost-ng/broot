import sys,os
sys.path.append(os.getcwd() + "\\..\\misc")
import colors
###################
#ABOUT SECTION
###################
name = ""
author = ""
version = "1.0"
art = ""
###################
#Executed on Import
###################
banner = '''
{}
{}
Author:  {}
Version: {}'''.format(art,name,author,version)
print(banner)
###################

#This is an example, you do not necessarily need extra commands
local_cmds = {

}

#This is an example, variables must have a unique name
local_vars = {
    'Threads': {
        "Name": "Threads",
        "Value": 1,
        "Type": 'Integer',
        "Default": "1 Thread",
        "Help": "Amount of concurrent threads to run.  High values may slow down your computer.",
        "Example": "10 (threads)"
    },
    'Wait-Period': {
        "Name": "Wait-Period",
        "Value": 0,
        "Type": 'Integer',
        "Default": "Wait 0 seconds in between attempts",
        "Help": "Amount of time in seconds to wait in between attempts.",
        "Example": "60 (secs)" 
    }
}


#This function does hte main exection of the brutefore method
def run():

    pass