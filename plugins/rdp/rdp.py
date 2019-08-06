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
import subprocess


###########################
#SECTION 1 - IMPORTS
###########################
# try:
#     import rdpy    #HERE
# except ModuleNotFoundError:
#     colors.PrintColor("WARN", "Unable to find 'rdpy', install?")   #HERE
#     ans = input("[Y/N] ")
#     if ans.lower() == "y":
#         requires.install('rdpy')   #HERE
#         import rdpy
#     else:
#         colors.PrintColor("FAIL", "'<new_module_here>' is a dependency!")   #HERE
#         input()

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
    'try-backdoor': {
        "Name": "Try-Backdoor",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "This option will try to determine if sticky keys or other backdoors will open a command prompt",
        "Example": "True"
    },
    'rdp-bin': {
        "Name": "RDP-Bin",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "Options are: rdesktop xfreerdp",
        "Example": "xfreerdp"
    },
    'rdp-path': {
        "Name": "RDP-Path",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "This is auto filled with a common binary/exe path.  You may still change it.",
        "Example": r"C:\Users\root\Documents\RDP\freerdp.exe"
    },
    'proxy-ip': {
        "Name": "Proxy-IP",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "The IP of your proxy server",
        "Example": "10.0.0.4"
    },
    'proxy-protocol': {
        "Name": "Proxy-Protocol",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "The options here are socks4 socks5 http",
        "Example": "socks5"
    },
    'proxy-port': {
        "Name": "Proxy-Port",
        "Value": 8080,
        "Type": 'Integer',
        "Default": 8080,
        "Help": "The listening port for the proxy service",
        "Example": "9050"
    }

}

#############################
#SECTION 5 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE
def run(username, password, target):
    print_fails = global_vars['print-failures']['Value']
    verbose = global_vars['verbose']['Value']
    attempt = "Target:{} Username:{} Password:{}".format(target, username, password)
    failed = False
    success = False
    if os.name == 'nt':
        colors.PrintColor("WARN","Windows is not supported at this time!")
        return
    rdp_bin = plugin_vars['rdp-bin']['Value']
    rdp_path = plugin_vars['rdp-path']['Value']
    proxy_proto = plugin_vars['proxy-protocol']['Value']
    proxy_port = plugin_vars['proxy-port']['Value']
    proxy_ip = plugin_vars['proxy-ip']['Value']
    if rdp_bin == "rdesktop":
        if rdp_path is None or "rdesktop" not in rdp_path:
            plugin_vars['rdp-path']['Value'] = "/usr/bin/rdesktop"
            rdp_bin = plugin_vars['rdp-path']['Value']
    elif rdp_bin == "xfreerdp":
        failure_lst = ["LOGON_FAILURE", "AUTHENTICATION_FAILED"]
        if rdp_path is None or "xfreerdp" not in rdp_path:
            plugin_vars['rdp-path']['Value'] = "/usr/bin/xfreerdp"
            rdp_bin = plugin_vars['rdp-path']['Value']
        cmd = "{} /v:{} /u:{} /p:{} /client-hostname:{} /cert-ignore +auth-only".format(rdp_bin,target,username,password,target,target)
        
        if proxy_ip is not None:
            append = "/proxy:{}://{}:{}".format(proxy_proto,proxy_ip,proxy_port)
            cmd = cmd + " " + append
            if verbose:
                print("cmd: " + cmd)
        result = subprocess.run(cmd.split(), capture_output=True)
        if verbose:
            print(result)
            #print("sterr: " + result.stderr.decode())
            #print("stdout: " + result.stdout.decode())
        for x in failure_lst:
            if x in str(result):
                failed = True
        if failed:
            success = False
            if verbose is True or print_fails is True :
                colors.PrintColor("INFO", "Failed Authentication --> {}".format(attempt))
        elif "proxy: failed" in str(result):
            success = False
            colors.PrintColor("FAIL", "Proxy Connection Error!")
        elif "Host unreachable" in str(result):
            colors.PrintColor("FAIL", "Host is unreachable!")
            success = False
        else:
            success = True

    return success