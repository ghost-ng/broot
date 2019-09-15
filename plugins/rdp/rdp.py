#TEMPLATE VERSION 1.0

##############################################
#SECTION 0 - DEFAULT IMPORTS (DO NOT CHANGE)
#############################################
import sys
import os
import subprocess
sys.path.append(os.path.join(os.getcwd(), "..", "..", "misc"))
from colors import print_good, print_fail, print_dbug, print_info, print_warn, print_stat
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import requires
from var import global_vars

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

Note: Unable to checks creds for RDP Security!
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
    # cmds = commands.split(" ")
    # if cmds[0] == "test":
    #     print("success!")
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
        "Value": "xfreerdp",
        "Type": 'String',
        "Default": None,
        "Help": "Currently only works with freerdp",
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
        "Value": None,
        "Type": 'Integer',
        "Default": None,
        "Help": "The listening port for the proxy service",
        "Example": "9050"
    }

}

def validate():
    if plugin_vars['proxy-protocol']['Value'] not in ['socks4', 'socks5', 'http', None]:
        print_fail("Proxy protocol must be socks4, socks5, or http")
        return False
#############################
#SECTION 5 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE
def run(username, password, target):
    skipped = []        #list of rdp servers with rdp security
    verbose = global_vars['verbose']['Value']
    if verbose:
        colors.PrintColor("INFO", "Running RDP Plugin")
    print_fails = global_vars['print-failures']['Value']
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

    failure_lst = ["LOGON_FAILURE", "AUTHENTICATION_FAILED"]
    if rdp_path is None or "xfreerdp" not in rdp_path:
        plugin_vars['rdp-path']['Value'] = "/usr/bin/xfreerdp"
        rdp_bin = plugin_vars['rdp-path']['Value']
    cmd = "{} /v:{} /u:{} /p:{} /client-hostname:{} /cert-ignore +auth-only /log-level:trace +sec-ext".format(rdp_bin,target,username,password,target)
    
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
    if "SSL_NOT_ALLOWED_BY_SERVER" in str(result) and "Negotiated RDP security" in str(result):
        if verbose:
            print_warn("Server Uses RDP Security, Unable to determine authentication status")
        skipped.append(target)
    elif "exit status 1" in str(result):
        success = False
        # print_fails is True:
        #     colors.PrintColor("INFO", "Failed Authentication --> {}".format(attempt))                
        if verbose is True:
            if "proxy: failed" in str(result):
                success = False
                colors.PrintColor("FAIL", "Proxy Connection Error!")
            if "Host unreachable" in str(result):
                colors.PrintColor("FAIL", "Host is unreachable!")
                success = False
    elif "exit status 0" in str(result):
        success = True
    else:
        success = False
        colors.PrintColor("WARN", "Unknown Result --> {}".format(attempt))

    return success