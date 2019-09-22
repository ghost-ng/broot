#TEMPLATE VERSION 1.0

##############################################
#SECTION 0 - DEFAULT IMPORTS (DO NOT CHANGE)
#############################################
import sys
import os
import subprocess
sys.path.append(os.path.join(os.getcwd(), "..", "..", "misc"))
from printlib import *
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import requires
from var import global_vars

###########################
#SECTION 1 - PLUGIN IMPORTS
###########################
# try:
#     import rdpy    #HERE
# except ModuleNotFoundError:
#     print_warn("Unable to find 'rdpy', install?")   #HERE
#     ans = input("[Y/N] ")
#     if ans.lower() == "y":
#         requires.install('rdpy')   #HERE
#         import rdpy
#     else:
#         print_fail("'<new_module_here>' is a dependency!")   #HERE
#         input()
from time import sleep
###########################
#SECTION 2 - ABOUT
###########################
name = ""
description = '''
The rdp plugin helps with probing the rdp service to determine valid credentials.\
This is a simple plugin that comes with the default 'broot' framework.
'''
author = "midnightseer"
version = "1.0"
art = """
              .--._
               `.  `-.
               .-'    `.
             .'      _..:._
            `.  .--.'      `.
            _.'  \.      .--.\\
          .'      |     |    |
         `--.     |  .--|    D
             `;  /'\/   ,`---'@
           .'  .'   '._ `-.__.'
         .'  .'      _.`---'
       .'--''   .   `-..__.--.
jgs ~-=  =-~_-   `-..___(  ===;
    ~-=  - -    .'       `---'

Check RDP creds as fast as Sonic! **almost as fast**

"""
banner = '''
{}
{}
Author:  {}
Version: {}'''.format(art,name,author,version)
print(banner)
print_warn("At this time this plugin is unable to determine authentication if the RDP server only uses RDP security")
sleep(2)

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
    if os.name == "posix":
        cmd = "whereis xfreerdp"
        result = subprocess.run(cmd.split(), capture_output=True)
        try:
            return result.stdout.split()[1].decode()
        except:
            pass
    else:
        pass
#############################
#SECTION 4 - PLUGIN VARIABLES
#############################

#This is an example, variables must have a unique name
plugin_vars = {
    'try-backdoor': {
        "Name": "Try-Backdoor",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "This option will try to determine if sticky keys or other backdoors will open a command prompt",
        "Example": "True"
    },
    'bin-path': {
        "Name": "Bin-Path",
        "Value": attempt_autodetect(),
        "Type": 'String',
        "Default": None,
        "Help": "Currently only works with freerdp",
        "Example": r"c:\users\miguel\documents\rdp\wfreerdp.exe"
    },
    'domain': {
        "Name": "Domain",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "The domain to authenticate to",
        "Example": "constoso.local"
    },
    'proxy': {
        "Name": "Proxy",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "Proxy settings in the form <protocol>://<ip>:<port>",
        "Example": "socks4://10.0.0.4:9050"
    },
    'debug': {
        "Name": "Debug",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "Prints the debug output",
        "Example": "set debug true"
    }
}

def validate():
    validated = True
    if plugin_vars['proxy']['Value'] is not None:
        proxy_setting = plugin_vars['proxy']['Value']
        try:
            temp = proxy_setting.split(":")
            if len(temp) != 3:
                validated = False
                print_fail("Unrecognized Proxy Setting.  Format should be: socks4://10.0.0.4:9050")
            if temp[0] not in ['socks4', 'socks5', 'http']:
                validated = False
                print_fail("Unrecognized Proxy Protocol.  Allowed Protocols are socks4 socks5 http.")
        except:
            print_fail("Unrecognized Proxy Setting.  Format should be: socks4://10.0.0.4:9050")
    if os.name == "nt" and plugin_vars['bin-path']['Value'] is None:
        print_fail("You must set a path for freerdp on Windows")
        validated = False
    if plugin_vars['bin-path']['Value'] is not None:
        if os.path.isfile(plugin_vars['bin-path']['Value']) is False:
            print_fail("Unable to find {}".format(plugin_vars['bin-path']['Value']))
            validated = False
        if "freerdp" not in plugin_vars['bin-path']['Value']:
            print_warn("freerdp is not in the binary path, continuing in case you re-named it...s")
    return validated
#############################
#SECTION 5 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE
def run(username, password, target):
    rdp_sec = []        #list of rdp servers with rdp security
    verbose = global_vars['verbose']['Value']
    if verbose:
        print_info("Running RDP Plugin")
    attempt = "Target:{} Username:{} Password:{}".format(target, username, password)
    failed = False
    success = False
    
    rdp_bin = plugin_vars['bin-path']['Value']
    failure_lst = ["LOGON_FAILURE", "AUTHENTICATION_FAILED"]
    
    cmd = "{} /v:{} /u:{} /p:{} /client-hostname:{} /cert-ignore +auth-only /log-level:trace".format(rdp_bin,target,username,password,target)
    
    if plugin_vars['proxy']['Value'] is not None:
        proxy_setting = plugin_vars['proxy']['Value']
        cmd = cmd + " " + "/proxy:" + proxy_setting
    if plugin_vars['domain']['Value'] is not None:
        domain = plugin_vars['domain']['Value']
        cmd = cmd + " " + "/d:" + domain
    if plugin_vars['debug']['Value']:
        print_dbug("cmd: " + cmd)
    try:
        result = subprocess.run(cmd.split(), capture_output=True)
    except Exception as e:
        print_fail("Unable to execute successfully")
        if verbose:
            print(e)
            print(sys.exc_info)
    if plugin_vars['debug']['Value'] is True:
        print_dbug(str(result))
    if "SSL_NOT_ALLOWED_BY_SERVER" in str(result) and "Negotiated RDP security" in str(result):
        if verbose:
            print_warn("Server Uses RDP Security, Unable to determine authentication status")
        rdp_sec.append(target)
    elif "exit status 1" in str(result):
        success = False
        # print_fails is True:
        #     print_info("Failed Authentication --> {}".format(attempt))                
        if verbose is True:
            if "proxy: failed" in str(result):
                success = False
                print_fail("Proxy Connection Error!")
            if "Host unreachable" in str(result):
                print_fail("Host is unreachable!")
                success = False
            if "ERRCONNECT_CONNECT_FAILED" in str(result) or "Broken pipe" in str(result):
                print_fail("Connection Failed! Is that IP alive?")
            if "ERRCONNECT_AUTHENTICATION_FAILED" in str(result):
                print_fail("Credentials failed!")
    elif "exit status 0" in str(result):
        success = True
    else:
        success = False
        print_warn("Unknown Result --> {}".format(attempt))

    return success