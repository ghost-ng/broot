#TEMPLATE VERSION 1.0

import sys
import os
sys.path.append(os.getcwd() + "\\..\\..\\misc")
import colors
import requires

try:
    import <new_module_here>
except ModuleNotFoundError:
    colors.PrintColor("WARN", "Unable to find '<new_module_here>', install?")
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('<new_module_here>')
    else:
        colors.PrintColor("FAIL", "'<new_module_here>' is a dependency!")

###################
#ABOUT SECTION
###################
name = ""
author = ""
version = "1.0"
art = """


"""
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
module_cmds = {

}

#function to define what to do with the new commands
def module_commands(cmds):
    pass

#This is an example, variables must have a unique name
module_vars = {
    'Threads': {
        "Name": "Threads",
        "Value": 1,
        "Type": 'Integer',
        "Default": 1,
        "Help": "Amount of concurrent threads to run.  High values may slow down your computer.",
        "Example": "10 (threads)"
    },
    'Wait-Period': {
        "Name": "Wait-Period",
        "Value": 0,
        "Type": 'Integer',
        "Default": 0,
        "Help": "Amount of time in seconds to wait in between attempts.",
        "Example": "Wait 0 seconds in between attempts" 
    }
}


#This function does the main exection of the brutefore method and MUST BE HERE
def run():

    pass