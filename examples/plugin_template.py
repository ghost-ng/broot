#TEMPLATE VERSION 1.0

##############################################
#SECTION 0 - DEFAULT IMPORTS (DO NOT CHANGE)
#############################################

import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "..", "misc"))
from printlib import *
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import requires
from var import global_vars


###########################
#SECTION 1 - IMPORTS
###########################
try:
    import <new_module_here>    #HERE
except ModuleNotFoundError:
    print_warn("WARN", "Unable to find '<new_module_here>', install?")   #HERE
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('<new_module_here>')   #HERE
        import <new_module_here>
    else:
        print_fail("'<new_module_here>' is a dependency!")   #HERE
        input()

###########################
#SECTION 2 - ABOUT
###########################
name = ""
description = '''
The <example> plugin helps with probing the ssh authentication service to determine valid credentials.\
This is a simple plugin that comes with the default 'broot' framework.
'''
author = ""
version = "1.0"
art = """


"""
banner = '''
{}
{}
Author:  {}
Version: {}'''.format(art,name,author,version)
print(banner)

#############################
#SECTION 3 - PLUGIN COMMANDS
#############################

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
def parse_plugin_cmds(commands):
    cmds = commands.split(" ")
    if cmds[0] == "test":
        print("success!")
    pass

#############################
#SECTION 4 - PLUGIN VARIABLES
#############################

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

#############################
#SECTION 5 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE
def run(username, password, target):
    attempt = "Target:{} Username:{} Password:{}".format(target, username, password)
    verbose = global_vars['verbose']['Value']
    pass