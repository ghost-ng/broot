#TEMPLATE VERSION 1.0

##############################################
#SECTION 0 - DEFAULT IMPORTS (DO NOT CHANGE)
#############################################

import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "..", "misc"))
import colors
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import requires
from var import global_vars


###########################
#SECTION 1 - IMPORTS
###########################
try:
    import telnetlib    #HERE
except ModuleNotFoundError:
    colors.PrintColor("WARN", "Unable to find 'telnetlib', install?")   #HERE
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('telnetlib')   #HERE
        import telnetlib
    else:
        colors.PrintColor("FAIL", "'telnetlib' is a dependency!")   #HERE
        input()

###########################
#SECTION 2 - ABOUT
###########################
name = ""
description = '''
The telnet plugin helps with probing the telnet authentication service to determine valid credentials.\
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
    'port': {
        "Name": "Port",
        "Value": 23,
        "Type": 'Integer',
        "Default": 23,
        "Help": "The target port with the telnet service listening",
        "Example": "23"
    },
    
}

#############################
#SECTION 5 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE
def run(target, username, password):
tn = telnetlib.Telnet(target)
tn.read_until("login: ")
tn.write(username + "\n")
tn.read_until("word: ")
tn.write(password + "\n")
print(tn.read_all())
