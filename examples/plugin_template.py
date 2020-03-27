#TEMPLATE VERSION 1.4

##############################################
#SECTION 0 - DEFAULT IMPORTS (DO NOT CHANGE)
#############################################
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import sys
import os

from printlib import *

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
#SECTION 5 - VALIDATE
#############################
#This function is used to validate your plugin variables prior to execution.  
#'Broot" calles this function immediately after 'run' and upon 'validate.'
#This function does not need to be filled out but the skeleton structure here
#is required. 

def validate():
    validated = True        # Do not change
    return validated

#############################
#SECTION 6 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE

#Default Port - if you have a default port to auto fill some variable, enter it here.
global_vars['target-port']['Value'] = ###

def run(username, password, target, port):
    attempt = "Target:{}:{} Username:{} Password:{}".format(target, port, username, password) # for printing messages if you want to
    verbose = global_vars['verbose']['Value']
    pass
    #return True or False  -- must return True if the authentication attempt was successful and false if it failed
