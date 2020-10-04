import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "..", "src"))
from printlib import *
import requires
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from var import global_vars, system_vars
MODULE_NAME = __file__.split("/")[len(__file__.split("/"))-1]
###########################
#SECTION 2 - ABOUT
###########################
name = "http-post"
description = '''
This plugin is used to bruteforce a simple HTTP POST request.  You'll
need the html for the username and password fields.

Extra Help: Use only the Target Fields for your url
Example: set target http://10.0.0.1:8443/Login.htm
'''
author = "midnightseer"
version = "1.01"
art = r"""
     ____
    |    |
    | .--'
,.--| |-------------.
|:\ | |   __       _ \
|#| | |              |
|#| |o|  THE BROOTS  |
|#| '-'              |
|#|                  |
 \|__________________|
   [_______________]
          \ \   | |
           \ \  | |
           '/~\ | |
"""
banner = '''
{}
{}
Author:  {}
Version: {}

Description: {}'''.format(art,name,author,version,description)
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
    'password-field-id': {
        "Name": "Password-Field-ID",
        "Value": 'password',
        "Type": 'String',
        "Default": 'password',
        "Help": "This value is the password id value from the html form.",
        "Example": "|<input id=password-id>| >>password-id<< is the value."
    },
    'username-field-id': {
        "Name": "Username-Field-ID",
        "Value": 'username',
        "Type": 'String',
        "Default": 'username',
        "Help": "This value is the password id value from the html form.",
        "Example": "|<input id=username-id>| >>username-id<< is the value." 
    },
    'submit-field-id': {
        "Name": "Submit-Field-ID",
        "Value": 'submit',
        "Type": 'String',
        "Default": "submit",
        "Help": "This value is the password id value from the html form.",
        "Example": "|<input id='submit' value='Login'>| >>submit<< is Field-ID." 
    },
    'submit-field-value': {
        "Name": "Submit-Field-Value",
        "Value": 'submit',
        "Type": 'String',
        "Default": "submit",
        "Help": "This value is the password id value from the html form.",
        "Example": "|<input id='submit' value='Login'>| >>Login<< is Field-Value." 
    },
    'skip-submit-field': {
        "Name": "Skip-Submit-Field",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "Some services do not add the submit id/value in the POST payload",
        "Example": "set skip-submit-field False" 
    },
    'check-login': {
        "Name": "Check-Login",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "If this value is NOT in the response html text, then the login succeeded",
        "Example": "set check-login password" 
    },
    'csrf-element-id': {
        "Name": "CSRF-Element-ID",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "The html element id containing the crsf token",
        "Example": "set csrf-element-id jstokenCSRF" 
    },
    'csrf-value-label': {
        "Name": "CSRF-Value-Label",
        "Value": 'value',
        "Type": 'String',
        "Default": 'value',
        "Help": "The csrf html element tag containing the crsf token value ie: csrf_value='sdfdsfsdfds34r3425'",
        "Example": "set csrf-value-tag csrf_value" 
    },
    'csrf-post-label': {
        "Name": "CSRF-Post-Label",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "The csrf post paramater label",
        "Example": "set csrf-post-label tokenCSRF" 
    },
    'csrf-initial-get': {
        "Name": "CSRF-Initial-Get",
        "Value": True,
        "Type": 'Boolean',
        "Default": True,
        "Help": "The csrf post paramater label",
        "Example": "set csrf-post-label tokenCSRF" 
    },
    'request-header': {
        "Name": "Request-Header",
        "Value": None,
        "Type": 'Multi-Line',
        "Default": None,
        "Help": "None --> proceed with default headers; custom --> add custom headers through an interactive prompt",
        "Example": "set request-header custom" 
    },
    'view-response': {
        "Name": "View-Response",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "View the web server's response.  Normally used to test configs as it will be very noisy on your screen.",
        "Example": "set view-response true" 
    },
    'min-password-length': {
        "Name": "Min-Password-Length",
        "Value": 1,
        "Type": "Integer",
        "Default": 1,
        "Help": "Set a minimum password length for your authentication attempts; this will skip password that do not meet this requirement.",
        "Example": "set min-password-length 5" 
    }
}

INITIAL_GET = False

#############################
#SECTION 5 - VALIDATE
#############################
#This function is used to validate your plugin variables prior to execution.  
#'Broot" calles this function immediately after 'run' and upon 'validate.'
#This function does not need to be filled out but the skeleton structure here
#is required. 

def validate():
    validated = True        # Technically, field values can have numbers, letters, and special chars, no validation needed
    if plugin_vars['password-field-id']['Value'] is None:
        validated = False
        print_fail("password-field-id is a required field")

    if plugin_vars['username-field-id']['Value'] is None:
        validated = False
        print_fail("username-field-id is a required field")

    if plugin_vars['submit-field-id']['Value'] is None:
        validated = False
        print_fail("submit-field-id is a required field")

    if plugin_vars['submit-field-value']['Value'] is None:
        validated = False
        print_fail("submit-field-value is a required field")

    if plugin_vars['check-login']['Value'] is None:
        validated = False
        print_fail("check-login is a required field")

    if "<" in plugin_vars['password-field-id']['Value'] or ">" in plugin_vars['password-field-id']['Value']:
        validated = False
        print_fail("password-field-id should not contain html brackets")

    if "<" in plugin_vars['username-field-id']['Value'] or ">" in plugin_vars['username-field-id']['Value']:
        validated = False
        print_fail("username-field-id should not contain html brackets")

    return validated

#############################
#SECTION 6 - MAIN
#############################
#This function does the main exection of the brutefore method and MUST BE HERE

#Default Port - if you have a default port to auto fill some variable, enter it here.
#global_vars['target-port']['Value'] = 80

def format_variable(variable, setting=None):
    temp_dict = ""
    if variable['Name'] == 'Request-Header':
        try:
            temp_dict = json.loads(setting.replace("'",'"'))
            return temp_dict
        except Exception as e:
            verbose = global_vars['verbose']['Value']
            #print_fail("Unable to set variable (is the right plugin loaded?)")
            if verbose:
                print_info("Unable to load into a dictionary")
                print("Setting:\n",setting)
                print_fail(str(e))
                print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
                print_fail("Error in Module - {}".format(MODULE_NAME))     

            print("Enter input, separate each item with ENTER [1st BLANK line ends the input session]")
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            text = '\n'.join(lines)
            return parse_header(text)
    else:
        return False

def parse_header(header_glob):
    header = {}
    temp_list = header_glob.split("\n")
    for item in temp_list:
        if item != "":
            header[item.split(":", 1)[0]] = item.split(":", 1)[1][1:]
    return header

def get_csrf_token(html):
    verbose = global_vars['verbose']['Value']
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html)
    match_html = soup.find_all(id=plugin_vars['csrf-element-id']['Value'])
    csrf_value = match_html[0][plugin_vars['csrf-value-label']['Value']]
    if verbose:
        print_info("Found csrf value \n{}".format(csrf_value))
    return csrf_value


def run(username, password, target, port):
    global INITIAL_GET
    if len(password) < plugin_vars['min-password-length']['Value']:
        print_warn("'{}' does not meet the length requirements".format(password))
        return None
    verbose = global_vars['verbose']['Value']
    if plugin_vars['skip-submit-field']['Value'] is True:
        post_payload = {
            plugin_vars['password-field-id']['Value']: password,
            plugin_vars['username-field-id']['Value']: username
            }
    else:
        post_payload = {
            plugin_vars['password-field-id']['Value']: password,
            plugin_vars['username-field-id']['Value']: username,
            plugin_vars['submit-field-id']['Value']: plugin_vars['submit-field-value']['Value']
            }
    post_header = plugin_vars['request-header']['Value']
    try:
        if plugin_vars['csrf-initial-get']['Value'] is True and INITIAL_GET is False:
                res = s.get(target)
                system_vars['HTTP-Session'] = res
                INITIAL_GET = True
            if plugin_vars['csrf-post-label']['Value'] is not None:
                csrf_value = get_csrf_token(res.html)
                csrf_dict = {plugin_vars['csrf-post-label']['Value']:csrf_value}
            post_payload.update(csrf_dict)
        s = requests.Session()
        if plugin_vars['post-header'] is not None:
            try:
                if "https" in target:
                    r = s.post(target, headers=post_header, data=post_payload,verify=False)
                else:
                    r = s.post(target, headers=post_header, data=post_payload)
            except requests.exceptions.ConnectionError:
                raise ConnectionAbortedError
            except TimeoutError:
                raise TimeoutError
        else:
            try:
                if "https" in target:
                    r = s.post(target, data=post_payload,verify=False)
                else:
                    r = s.post(target, data=post_payload)
            except requests.exceptions.ConnectionError:
                raise ConnectionAbortedError
            except TimeoutError:
                raise TimeoutError
        if r.status_code != 200 and verbose is True:
            print_fail("Uh oh, something is wrong...received server response {}".format(str(r.status_code)))
        elif r.status_code != 200 and verbose is False:
            print_fail("Server Replied with a non-200 response code!")

        if plugin_vars['view-response']['Value'] is True:
            print(r.text)
        if plugin_vars['check-login']['Value'] in r.text:
            return False
        else:
            if r.status_code == 200:
                return True
            else:
                return False
    except Exception as e:
        if verbose:
            print_fail(str(e))
            print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
            print_fail("Error in Module - {}".format(MODULE_NAME))
        return False