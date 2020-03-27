import sys
import os
from printlib import *
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import requires
from var import global_vars

try:
    import paramiko
except ModuleNotFoundError:
    print_warn("Unable to find 'paramiko', install?")
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('paramiko')
        import paramiko
    else:
        print_fail("'Paramiko' is a dependency!")
        input()
    
###################
#ABOUT SECTION
###################
name = "ssh broot-forcer"
description = '''
The SSH plugin helps with probing the ssh authentication service to determine valid credentials.\
This is a simple plugin that comes with the default 'broot' framework.
'''
author = "midnightseer"
version = "1.0"
art = '''
                    $$\       
                    $$ |      
 $$$$$$$\  $$$$$$$\ $$$$$$$\  
$$  _____|$$  _____|$$  __$$\ 
\$$$$$$\  \$$$$$$\  $$ |  $$ |
 \____$$\  \____$$\ $$ |  $$ |
$$$$$$$  |$$$$$$$  |$$ |  $$ |
\_______/ \_______/ \__|  \__|'''

###################
#Executed on Import
###################
banner = '''
{}
{}
Author:  {}
Version: {}'''.format(art, name, author, version)
print(banner)

###################

#This is an example, you do not necessarily need extra commands
plugin_cmds = {
    # "test": {
    #         "Command": "test",
    #         "Help": "Print information related to the subsequent key-word.",
    #         "Sub-Cmds": ["commands", "plugins", "options", "loaded-plugin", "creds", "sequence"],
    #         "Usage": "test <sub-cmd>",
    #         "Alias": None
    #     }
}

def parse_plugin_cmds(cmds):
    if cmds[0] == "test":
        print("success!")
    pass

#This is an example, variables must have a unique name
plugin_vars = {    
    "timeout": {
        "Name": "Timeout",
        "Value": 3,
        "Type": 'Integer',
        "Default": 3,
        "Help": "Amount of seconds for the TCP timeout.",
        "Example": "10 (seconds)"
    }, 
    "banner-timeout": {
        "Name": "Banner-Timeout",
        "Value": 10,
        "Type": 'Integer',
        "Default": 10,
        "Help": "Amount of seconds to wait for the SSH banner.",
        "Example": "10 (seconds)"
    },
    "allow-hosts": {
        "Name": "Allow-Hosts",
        "Value": True,
        "Type": 'Boolean',
        "Default": True,
        "Help": "Allow unknown hosts to connect to.",
        "Example": "Yes, connect to unknown hosts."
    }
}


#This function does the main exection of the brutefore method

#Default Port
var.global_vars['target-port']['Value'] = 22

def run(username, password, target, port):
    success = False
    verbose = global_vars['verbose']['Value']
    timeout = plugin_vars['timeout']['Value']
    port = var.global_vars['target-port']['Value']
    banner_timeout = plugin_vars['banner-timeout']['Value']
    attempt = "Target:{}:{} Username:{} Password:{}".format(target, port, username, password)

    try:
        client = paramiko.SSHClient()
        if plugin_vars['allow-hosts']['Value']:  
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if verbose:
            print_info("Trying " + attempt)
        client.connect(target, username=username, password=password, timeout=timeout, banner_timeout=banner_timeout, port=port)
        client.close()
        success = True
    except paramiko.AuthenticationException:
        if verbose:
            print_info("Failed Authentication --> {}".format(attempt))
    except paramiko.SSHException as sshException:
        if verbose:    
            print_fail("Fail --> {} Could not establish SSH connection".format(attempt))
    except Exception as e:
        if verbose:
            print_fail("Fail --> {} Error! {}".format(attempt, e))
    finally:
        return success
        