#TEMPLATE VERSION 1.0

##############################################
#SECTION 0 - DEFAULT IMPORTS (DO NOT CHANGE)
#############################################
import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
from printlib import *
import requires
from var import global_vars

###########################
#SECTION 1 - PLUGIN IMPORTS
###########################
try:
    import imaplib    #HERE
except ModuleNotFoundError:
    print_warn("Unable to find 'imaplib', install?")   #HERE
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('imaplib')   #HERE
        import rdpy
    else:
        print_fail("'imaplib' is a dependency!")   #HERE
        input()

###########################
#SECTION 2 - ABOUT
###########################
name = ""
description = '''
The IMAP plugin allows you to test credentials using the python3 imap library
'''
author = "midnightseer"
version = "1.0"
art = r"""
                              ________
 IIIIIIIIIIIII           ,o88~~88888888o,
       I                ,~~?8P  88888     8,
       I               d  d88 d88 d8_88     b
       I              d  d888888888          b
       I              8,?88888888  d8.b o.   8
 IIIIIIIIIIIII        8~88888888~ ~^8888\ db 8
                      ?  888888          ,888P
                       ?  `8888b,_      d888P
                        `   8888888b   ,888'
                          ~-?8888888 _.P-~
                               ~~~~~~                            
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
    # cmds = commands.split(" ")
    # if cmds[0] == "test":
    #     print("success!")
    pass

#############################
#SECTION 4 - PLUGIN FUNCTIONS
#############################

def attempt_autodetect():
    pass
#############################
#SECTION 4 - PLUGIN VARIABLES
#############################

#This is an example, variables must have a unique name
plugin_vars = {
    
}

def validate():
    validated = True
    
    return validated
#############################
#SECTION 5 - MAIN
#############################

#Default Port
global_vars['target-port']['Value'] = 143

#This function does the main exection of the brutefore method and MUST BE HERE
def run(username, password, target, port):
    
    verbose = global_vars['verbose']['Value']
    if verbose:
        print_info("Running IMAP Plugin")
    attempt = "Target:{}:{} Username:{} Password:{}".format(target, port, username, password)
    try:
        if verbose:
            print_info(attempt)
        M = imaplib.IMAP4(target)
        M.login("test","rwet")
        M.shutdown()
        return True
    except Exception as e:
        M.shutdown()
        if verbose:
            print_info("Error: {}".format(e))
        if "Login failed" in str(e.decode()):
            return False
