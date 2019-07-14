#This file a list of all the common variables available to any given
import os,sys
from prettytable import PrettyTable
sys.path.append(os.getcwd() + "\\..\\misc")
import colors
import importlib

#GLOBALS
global_cmds = {}

global_vars = {
    'threads': {
        "Name": "Threads",
        "Value": 1,
        "Type": 'Integer',
        "Default": "1 Thread",
        "Help": "Amount of concurrent threads to run.  High values may slow down your computer.",
        "Example": "10 (threads)"
    },
    'wait-period': {
        "Name": "Wait-Period",
        "Value": 0,
        "Type": 'Integer',
        "Default": "Wait 0 seconds in between attempts",
        "Help": "Amount of time in seconds to wait in between attempts.",
        "Example": "60 (secs)" 
    },
    'wait-interval': {
        "Name": "Wait-Interval",
        "Value": 1,
        "Type": 'Integer',
        "Default": "After 1 attempt, wait the desired [wait time] seconds.",
        "Help": "Amount of attempts in between each wait period",
        "Example": "3 (attempts)"
    },
    're-try': {
        "Name": "Re-Try",
        "Value": 0,
        "Type": 'Integer',
        "Default": "Re-Try the given combination 0 times after a failure.",
        "Help": "Amount of times to re-try a set of credentials, even after a failure.  Normally 0.",
        "Example": "0 (tries)"
    },
    'password-file': {
        "Name": "Password-File",
        "Value": None,
        "Type": 'String',
        "Default": "[empty]",
        "Help": "A list of usernames, 1 per line, in a file.",
        "Example": r"C:\Users\MidnightSeer\Documents\passwords.lst"
    },
    # 'passwords': {
    #     "Name": "Passwords",
    #     "Value": None,
    #     "Type": 'String',
    #     "Default": "[empty]",
    #     "Help": "A comma seperated list of passwords.",
    #     "Example": "toor,password12324,qaz123456"
    # },
    'password': {
        "Name": "Password",
        "Value": None,
        "Type": 'String',
        "Default": "[empty]",
        "Help": "A single password to try.",
        "Example": "P@ssword"
     },
    'username-file': {
        "Name": "Username-File",
        "Value": None,
        "Type": 'String',
        "Default": "[empty]",
        "Help": "A list of usernames, 1 per line, in a file.",
        "Example": r"C:\Users\MidnightSeer\Documents\username.lst"
    },
    # 'usernames': {
    #     "Name": "Usernames",
    #     "Value": None,
    #     "Type": 'String',
    #     "Default": "[empty]",
    #     "Help": "A comma seperated list of usernames.",
    #     "Example": "username1,root,username3"
    # },
    'username': {
        "Name": "Username",
        "Value": None,
        "Type": 'String',
        "Default": "[empty]",
        "Help": "A single username to try",
        "Example": "root"
     },
    'target-file': {
        "Name": "Target-File",
        "Value": None,
        "Type": 'String',
        "Default": "[empty]",
        "Help": "A list of IPs and/or Fully Qualified Domain Names, 1 per line, in a file.",
        "Example": r"C:\Users\MidnightSeer\Documents\targets.lst"
    },
    'targets': {
        "Name": "Targets",
        "Value": None,
        "Type": 'String',
        "Default": "[empty]",
        "Help": "A comma seperated list of IPs or Fully Qualiifed Domain Names.",
        "Example": "12.232.223.12,root.net,hackme.com"
    },
    'target': {
        "Name": "Target",
        "Value": None,
        "Type": 'String',
        "Default": "[empty]",
        "Help": "Single IP or Fully Qualified Domain Name.",
        "Example": "root.target.net"
    }
    # 'credentials': {
    #     "Name": "Credentials",
    #     "Value": None,
    #     "Type": 'String',
    #     "Default": "[empty]",
    #     "Help": "Sequence of Usernames and Passwords, seperated by a colon and comma.",
    #     "Example": "username:password,root:toor"
    # },
    # 'credentials-file': {
    #     "Name": "Credentials-File",
    #     "Value": None,
    #     "Type": 'String',
    #     "Default": "[empty]",
    #     "Help": "Sequence of Usernames and Passwords, seperated by a colon, per line.",
    #     "Example": r"C:\Users\MidnightSeer\Documents\creds.lst"
    # }
}

module_info = { 
    "Loaded-Module": {
        'Name': None,
        'Object': None
    },
    "Available-Modules": {}
}

def print_var_desc():
    for d in global_vars:
        item = global_vars[d]
        info = """
        {name}:
        Description: {h}
        Default: {d}
        Type: {t}
        Example: {e}""".format(name=item['Name'], h=item['Help'], d=item['Default'],
                    t=item['Type'], e=item['Example'])
        print(info)

def import_module(name):
    loaded_module = importlib.import_module(name, package=None)
    module_info['Loaded-Module']['Object'] = loaded_module
    module_info['Loaded-Module']['Name'] = name

def refresh_modules():
    module_info["Available-Modules"] = {}
    root = os.getcwd()
    path = root + "\..\modules"
    dir_list = os.walk(path)
    for f in dir_list:
        if len(f[2]) > 0:
            for d in f[2]:
                dict_name = d.rstrip(".py")
                if ".pyc" not in dict_name:
                    dict_value = {
                        "Name": dict_name,
                        "Path": f[0]
                    }
                    module_info["Available-Modules"].update({dict_name: dict_value})
    update_cmds()

def count_modules():
    count = len(module_info['Available-Modules'])
    return count

def show_modules():
    module_list = []
    colors.PrintColor("INFO", "Available Modules:")
    count = 0
    for module in module_info['Available-Modules'].keys():
        if count < 5:
            print(module + "  ", end="")
        else:
            print(module)
        count += 1
    print()
    msg = "Total: {}".format(count_modules())
    colors.PrintColor("INFO", msg)

def opts_to_table(var_type):
    table = PrettyTable(['Name', 'Value', 'Example'])
    if var_type.lower() == "global":
        table.title = "Global Variables"
        v = global_vars
    else:
        table.title = "Module Variables"
        loaded_module = module_info['Loaded-Module']['Object']
        v = loaded_module.module_vars
    for d in v:
        table.add_row([v[d]['Name'], v[d]['Value'], v[d]['Example']])
    colors.PrintColor("Success", "{} Variables:".format(var_type.capitalize()))
    print(table)


def print_enum_dict(tree, m, d=0):
    if m == "tree":
        marker = " --> "
    else:
        marker = ": "
    if (tree == None or len(tree) == 0):
        msg = "\t" * d + "-"
        print(msg)
    else:
        for key, val in tree.items():
            if (isinstance(val, dict)):
                print()
                msg = "\t" * d + key
                colors.PrintColor("STATUS", msg)
                print_enum_dict(val, d+1)
            else:
                msg = "\t" * d + str(key) + marker
                print(msg,end="")
                if type(val) is list:
                    print(*val)
                else:
                    print(val)

def vars_to_list(var):
    s=[]
    for v in var: 
        s.append(v)
    return s

def avail_mods_to_list():
    if len(module_info['Available-Modules']) > 0:
        a=[]
        for module in module_info['Available-Modules']:
            #print(module)
            a.append(module)
        return a

def reload_loaded_module():
    m = module_info['Loaded-Module']['Object']
    try:
        importlib.reload(m)
        colors.PrintColor("SUCCESS", "Successfully reloaded module")
    except:
        colors.PrintColor("FAIL", "Unable to load module")
        print(sys.exc_info())


def unload_module():
    m = module_info['Loaded-Module']['Object']
    del m
    wipe_loaded_module_info()

def get_loaded_module_name():
    if module_info["Loaded-Module"]['Name'] is not None:
        return module_info["Loaded-Module"]['Name']
    else:
        return "No Module Loaded"

def get_loaded_module_object():
    if check_module_loaded():
        return module_info["Loaded-Module"]['Object']
    else:
        return "No Module Loaded"

def check_module_loaded():
    if module_info["Loaded-Module"]['Name'] is None:
        return False
    else:
        return True

def wipe_loaded_module_info():
    module_info['Loaded-Module']['Name'] = None
    module_info['Loaded-Module']['Object'] = None

def load_module(module_name):
    module_info['Loaded-Module']['Name'] = module_name

def update_cmds():
    global global_cmds
    if check_module_loaded():    
        loaded_module = get_loaded_module_object()
        set_vars = vars_to_list(global_vars) + vars_to_list(loaded_module.module_vars)
    else:
        set_vars = vars_to_list(global_vars)
    global_cmds = {
        "show":["commands", "help", "modules", "options", "loaded-module"],
        "reload": [get_loaded_module_name()],
        "unload": [get_loaded_module_name()],
        "set": set_vars,
        "use": avail_mods_to_list(),
        "load": ["alias for 'use'"],
        "run": "",
        "broot": ["alias for 'run'"],
        "exit": "",
        "x": ["alias for 'exit'"],
        "quit": ["alias for 'exit'"],
        "q": ["alias for 'exit'"],
    }