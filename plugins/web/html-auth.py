#TEMPLATE VERSION 1.4

##############################################
#SECTION 0 - DEFAULT IMPORTS (DO NOT CHANGE)
#############################################
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import sys
import os
from printlib import *
import requires
from var import global_vars, system_vars
MODULE_NAME = __file__.split("/")[len(__file__.split("/"))-1]

###########################
#SECTION 1 - Module IMPORTS
###########################
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###########################
#SECTION 2 - ABOUT
###########################
name = "html-auth"
description = '''
Perform simple authentication with the http basic authentication module.
'''
author = "midnightseer"
version = "1.0"
art = """
  /\ ___ /\
 (  o   o  ) 
  \  >#<  /
  /       \  
 /         \       ^
|           |     //
 \         /    //
  ///  ///   --

-- YOU BASIC --

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
    'basic-auth': {
        "Name": "Basic-Auth",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "Perform http basic authentication",
        "Example": "set basic-auth true"
    },
    'digest-auth': {
        "Name": "Digest-Auth",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "Perform http digest authentication",
        "Example": "set digest-auth true" 
    },
    'check-login': {
        "Name": "Check-Login",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "If this value is NOT in the response html text, then the login succeeded",
        "Example": "set check-login password" 
    },
}

#############################
#SECTION 5 - VALIDATE
#############################
#This function is used to validate your plugin variables prior to execution.  
#'Broot" calls this function immediately after 'run' and upon 'validate.'
#This function does not need to be filled out but the skeleton structure here
#is required. 

def validate():
    validated = True        # Do not change

    if plugin_vars['basic-auth']['Value'] is False and plugin_vars['digest-auth']['Value'] is False:
        validated = False
        print_fail("You must specify an authenticaiton method")
    if plugin_vars['check-login']['Value'] is None:
        validated = False
        print_fail("You must specify a way to verify a logon attempt worked")
    return validated

#############################
#SECTION 6 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE

#Default Port - if you have a default port to auto fill some variable, enter it here.
#global_vars['target-port']['Value'] = ###

def run(username, password, target, port):
    attempt = "Target:{}:{} Username:{} Password:{}".format(target, port, username, password) # for printing messages if you want to
    verbose = global_vars['verbose']['Value']
    try:
        if plugin_vars['basic-auth']['Value'] is True:
            r = requests.get(target, auth=HTTPBasicAuth(username, password))

        elif plugin_vars['digest-auth']['Value'] is True:
            r = requests.get(target, auth=HTTPDigestAuth(username, password))

        if r.status_code != 200 and verbose is True:
                print_fail("Uh oh, something is wrong...received server response {}".format(str(r.status_code)))
            elif r.status_code != 200 and verbose is False:
                print_fail("Server Replied with a non-200 response code!")

        if plugin_vars['check-login']['Value'] not in r.text:
            return True
        else:
            return False

    except Exception as e:
        if verbose:
            print_fail(str(e))
            print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
            print_fail("Error in Module - {}".format(MODULE_NAME))
        return False
    #return True or False  -- must return True if the authentication attempt was successful and false if it failed
