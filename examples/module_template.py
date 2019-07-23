#TEMPLATE VERSION 1.0

import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "..", "misc"))
import colors
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import requires
from var import global_vars

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

#This is an example, you do not necessarily need extra commands.  Replace the below with your own
plugin_cmds = {
    # "test": {
    #         "Command": "test",
    #         "Help": "Print information related to the subsequent key-word.",
    #         "Sub-Cmds": ["commands", "plugins", "options", "loaded-plugin", "creds", "sequence"],
    #         "Usage": "test <sub-cmd>",
    #         "Alias": None
    #     },
}

#function to define what to do with the new commands
def parse_plugin_cmds(cmds):
    if cmds[0] == "test":
        print("success!")
    pass

#This is an example, variables must have a unique name
plugin_vars = {
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