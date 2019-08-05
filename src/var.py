#This file a list of all the common variables available to any given
import os
import sys
import requires
import importlib
from time import sleep
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
import colors


try:
    from prettytable import PrettyTable
except ModuleNotFoundError:
    colors.PrintColor("WARN", "Unable to find 'Prettytable', install?")
    ans = input("[Y/N] ")
    if ans.lower() == "y":
        requires.install('prettytable')
        from prettytable import PrettyTable
    else:
        colors.PrintColor("FAIL", "'Prettytable' is a dependency")
        input()

#GLOBALS
global_cmds = {}

global_vars = {
    'threads': {
        "Name": "Threads",
        "Value": 1,
        "Type": 'Integer',
        "Default": 1,
        "Help": "Amount of concurrent threads to run.  High values may slow down your computer.",
        "Example": "set threads 10"
    },
    'wait-time': {
        "Name": "Wait-Time",
        "Value": 0,
        "Type": 'Integer',
        "Default": 0,
        "Help": "Amount of time in seconds to wait in between wait-intervals.",
        "Example": "set wait-time 5" 
    },
    'wait-interval': {
        "Name": "Wait-Interval",
        "Value": 1,
        "Type": 'Integer',
        "Default": 1,
        "Help": "Amount of attempts in between each wait period.  This will never be 0.",
        "Example": "set wait-interval 5"
    },
    'wait-on-failure': {
        "Name": "Wait-On-Failure",
        "Value": 0,
        "Type": 'Integer',
        "Default": 0,
        "Help": "If greater than 0, each failed attempt will trigger a waiting period",
        "Example": "set wait-on-failure 5"
    },
    're-try': {
        "Name": "Re-Try",
        "Value": 0,
        "Type": 'Integer',
        "Default": 0,
        "Help": "Amount of times to re-try a set of credentials, even after a failure.  Normally 0.",
        "Example": "set re-try 2"
    },
    'password-file': {
        "Name": "Password-File",
        "Value": None,
        "Type": 'String',
        "Default": None,
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
        "Default": None,
        "Help": "A single password to try.",
        "Example": "P@ssword"
     },
    'username-file': {
        "Name": "Username-File",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "A list of usernames, 1 per line, in a file.",
        "Example": r"C:\Users\MidnightSeer\Documents\username.lst"
    },
    'usernames': {
        "Name": "Usernames",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "A comma seperated list of usernames. If a username consists of a comma, it needs to be in a file.",
        "Example": "username1,root,username3"
    },
    'username': {
        "Name": "Username",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "A single username to try",
        "Example": "root"
     },
    'target-file': {
        "Name": "Target-File",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "A list of IPs and/or Fully Qualified Domain Names, 1 per line, in a file.",
        "Example": r"C:\Users\MidnightSeer\Documents\targets.lst"
    },
    'targets': {
        "Name": "Targets",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "A comma seperated list of IPs or Fully Qualiifed Domain Names.",
        "Example": "12.232.223.12,root.net,hackme.com"
    },
    'target': {
        "Name": "Target",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "Single IP or Fully Qualified Domain Name.",
        "Example": "root.target.net"
    },
    "verbose": {
        "Name": "Verbose",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "Will print verbose messages.",
        "Example": "set verbose true"
    },
    "print-failures": {
        "Name": "Print-Failures",
        "Value": False,
        "Type": 'Boolean',
        "Default": False,
        "Help": "Print failures as well as successes.  By default broot only prints successes.",
        "Example": "set print-failures true"
    },
    "stop-on-success": {
        "Name": "Stop-on-Success",
        "Value": None,
        "Type": 'String',
        "Default": None,
        "Help": "If set to True, then stop testing creds against a given target after a successful authentication",
        "Example": "set stop-on-success target,username"
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

system_vars = {
    "valid-creds": {
        "Name": "Valid-Creds",
        "Credentials": [],
        "Usernames": [],
        "Targets": [],
        "Help": "List credentials for successful authentications",
    },
    "Loaded-Plugin": {
        'Name': None,
        'Object': None
    },
    "Available-Plugins": {}
}

def gen_random(command):
    #command will be in the form of 'random 1-10' or 'random'
    from random import randint
    cmds = command.split(" ")
    if len(cmds) > 1:
        temp = cmds[1].split("-")
        return randint(int(temp[0]), int(temp[1]))
    else:
        return randint(1, 30)

def file_exists(filename):
    exists = os.path.isfile(filename)  # initial check 
    #colors.PrintColor("FAIL","File does not exist, try again")    
    try:
        if filename is not None:
            while exists is False:
                colors.PrintColor("FAIL", "File does not exist, try again")
                file = input("[New File]: ")
                return file_exists(file)
    except KeyboardInterrupt:
        filename = None
    return filename

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

def save_creds(creds):

    target, username, password = creds
    plugin_name = get_loaded_plugin_name()
    success = "Plugin:{} Target:{} Username:{} Password:{}".format(plugin_name, target, username, password)
    saved_creds = system_vars['valid-creds']['Credentials']
    saved_creds.append(success)
    system_vars['valid-creds']['Credentials'] = saved_creds

    u_list = system_vars['valid-creds']['Usernames']
    u_list.append(username)
    system_vars['valid-creds']['Usernames'] = u_list

    t_list = system_vars['valid-creds']['Targets']
    t_list.append(target)
    system_vars['valid-creds']['Targets'] = t_list


def print_successes():
    count = 0
    for cred in system_vars['valid-creds']['Credentials']:
        count += 1
        print(cred)

def import_plugin(name):
    loaded_plugin = importlib.import_module(name, package=None)
    system_vars['Loaded-Plugin']['Object'] = loaded_plugin
    system_vars['Loaded-Plugin']['Name'] = name

def refresh_plugins():
    system_vars["Available-Plugin"] = {}
    root = os.getcwd()
    path = root + "\..\plugins"
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
                    system_vars["Available-Plugins"].update({dict_name: dict_value})
    update_cmds()

def count_plugins():
    count = len(system_vars['Available-Plugins'])
    return count

def show_plugins():
    plugin_list = []
    colors.PrintColor("INFO", "Available Plugins:")
    count = 0
    for plugin in system_vars['Available-Plugins'].keys():
        if count < 5:
            print(plugin + "  ", end="")
        else:
            print(plugin)
        count += 1
    print()
    msg = "Total: {}".format(count_plugins())
    colors.PrintColor("INFO", msg)

def opts_to_table(var_type):
    table = PrettyTable(['Name', 'Value', 'Example'])
    if var_type.lower() == "global":
        table.title = "Global Variables"
        v = global_vars
    else:
        table.title = "Plugin Variables"
        loaded_plugin = system_vars['Loaded-Plugin']['Object']
        v = loaded_plugin.plugin_vars
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
    if len(system_vars['Available-Plugins']) > 0:
        a=[]
        for plugin in system_vars['Available-Plugins']:
            #print(plugin)
            a.append(plugin)
        return a

def reload_loaded_plugin():
    m = system_vars['Loaded-Plugin']['Object']
    try:
        importlib.reload(m)
        colors.PrintColor("SUCCESS", "Successfully reloaded plugin")
    except:
        colors.PrintColor("FAIL", "Unable to load plugin")
        print(sys.exc_info())

def unload_plugin():
    m = system_vars['Loaded-Plugin']['Object']
    del m
    wipe_loaded_plugin_info()

def get_loaded_plugin_name():
    if system_vars["Loaded-Plugin"]['Name'] is not None:
        return system_vars["Loaded-Plugin"]['Name']
    else:
        return "No Plugin Loaded"

def get_loaded_plugin_object():
    if check_plugin_loaded():
        return system_vars["Loaded-Plugin"]['Object']
    else:
        return "No Plugin Loaded"

def check_plugin_loaded():
    if system_vars["Loaded-Plugin"]['Name'] is None:
        return False
    else:
        return True

def get_help(cmds):
    if len(cmds) > 1:
        try:
            #Check for the key-word as an alias
            for cmd in global_cmds:
                try:
            #check for aliases first
                    if cmds[1] in global_cmds[cmd]['Alias']:
                        print_enum_dict(global_cmds[cmd], m="vars")
                    elif check_plugin_loaded():
                        loaded_plugin = get_loaded_plugin_object()
                        if cmds[1] in loaded_plugin.plugin_cmds[cmd]['Alias']:
                            print_enum_dict(loaded_plugin.plugin_cmds[cmd], m="vars")
                except (TypeError, KeyError):
                    pass
            #Check for the key-word in global commands
            if cmds[1] in global_cmds.keys():
                print_enum_dict(global_cmds[cmds[1]], m="vars")
                print()
            #Check for the key-word in global variables
            elif cmds[1] in global_vars.keys():
                print_enum_dict(global_vars[cmds[1]], m="vars")
                print()
            #Check for the key-word in plugin variables
            elif check_plugin_loaded():
                loaded_plugin = get_loaded_plugin_object()
                if cmds[1] in loaded_plugin.plugin_cmds.keys():
                    print_enum_dict(loaded_plugin.plugin_cmds[cmds[1]], m="vars")
                    print()
                if cmds[1] in loaded_plugin.plugin_vars.keys():
                    print_enum_dict(loaded_plugin.plugin_vars[cmds[1]], m="vars")
                    print()
                if cmds[1] == get_loaded_plugin_name():
                    description = ("""Plugin: {}\nDescription: {}""".format(get_loaded_plugin_name(), loaded_plugin.description))
                    print(description)
                    print_enum_dict(loaded_plugin.plugin_cmds, m="vars")
                    print()
                    print_enum_dict(loaded_plugin.plugin_vars, m="vars")
                    print()
            else:
                print("Help topic does not exist!")
        except:
            print("Error in looking up help entry!")
            if global_vars['verbose']['Value']:
                print(sys.exc_info())
    else:
        colors.PrintColor("INFO", "Printing Global Variables:")
        sleep(.5)
        print_enum_dict(global_vars, m="vars")
        print()
        colors.PrintColor("INFO", "Printing Global Commands:")
        sleep(.5)
        print_enum_dict(global_cmds, m="vars")
        print()
        if check_plugin_loaded():
            loaded_plugin = get_loaded_plugin_object()
            print()
            colors.PrintColor("INFO", "Printing Plugin Variables:")
            sleep(.5)
            print_enum_dict(loaded_plugin.plugin_vars, m="vars")
            print()
            colors.PrintColor("INFO", "Printing Plugin Commands:")
            sleep(.5)
            print_enum_dict(loaded_plugin.plugin_cmds, m="vars")

def print_cmds(cmds):
    count = 1
    for d in cmds:
        if " " not in d:
            if count < 4:
                print(d, end="\t")
                count += 1
            else:
                print(d)
                count = 1
    print()

def wipe_loaded_plugin_info():
    system_vars['Loaded-Plugin']['Name'] = None
    system_vars['Loaded-Plugin']['Object'] = None

def load_plugin(plugin_name):
    system_vars['Loaded-Plugin']['Name'] = plugin_name

def get_available_cmds():
    avail_cmds = []
    #get list of main commands
    for i in global_cmds.keys(): avail_cmds.append(i)
    
    #get list of aliases
    for i in global_cmds.keys(): avail_cmds.append(global_cmds[i]['Alias'])
    
    #get commands in the loaded plugin
    if check_plugin_loaded():
        loaded_plugin = get_loaded_plugin_object()
        for i in loaded_plugin.plugin_cmds.keys(): avail_cmds.append(i)
        try:
            for i in global_cmds.keys(): avail_cmds.append(global_cmds[i]['Alias'])
        except KeyError:
            pass
    #remove all none values
    temp_list = [x for x in avail_cmds if x != None]
    #flatten the list
    new_cmd_list = []
    for item in temp_list:
        if isinstance(item, list):
            for i in item:
                new_cmd_list.append(i)
        else:
            new_cmd_list.append(item)
    return new_cmd_list

def update_cmds():
    global global_cmds
    if check_plugin_loaded():    
        loaded_plugin = get_loaded_plugin_object()
        set_vars = vars_to_list(global_vars) + vars_to_list(loaded_plugin.plugin_vars)
    else:
        set_vars = vars_to_list(global_vars)
    global_cmds = {
        "show": {
            "Command": "show",
            "Help": "Print information related to the subsequent key-word.",
            "Sub-Cmds": ["commands", "plugins", "options", "loaded-plugin", "creds", "sequence"],
            "Usage": "show <sub-cmd>",
            "Alias": None
        },
        "show commands": {
            "Command": "show commands",
            "Help": "Print all available commands with the main broot plugin and, if loaded, the loaded plugin.",
            "Sub-Cmds": None,
            "Usage": "show commands",
            "Alias": None
        },
        "show plugins": {
            "Command": "show plugins",
            "Help": "List all plugins that are available to be imported.  All plugins must be in the 'plugin' folder.",
            "Sub-Cmds": None,
            "Usage": "show plugins",
            "Alias": None
        },
        "show options": {
            "Command": "show options",
            "Help": "Print all available and configurable parameters.",
            "Sub-Cmds": None,
            "Usage": "show options",
            "Alias": None
        },
        "show loaded-plugin": {
            "Command": "show loaded-plugin",
            "Help": "List the currently loaded plugin.  The will only produce a meaningful result after 'load <plugin>' successfully executes",
            "Sub-Cmds": ["name", "object"],
            "Usage": "show loaded-plugin",
            "Alias": None
        },
        "show creds": {
            "Command": "show creds",
            "Help": "List all credentials that resulted in a successful authentication.",
            "Sub-Cmds": None,
            "Usage": "show creds",
            "Alias": None
        },
        "show sequence": {
            "Command": "show sequence",
            "Help": "Print the sequence string.  This can be pasted in a later broot prompt to quickly load an exact copy of the current configuration.",
            "Sub-Cmds": None,
            "Usage": "show sequence",
            "Alias": None
        },
        "help": {
            "Command": "help",
            "Help": "Print the help files.  Alone, the command prints the entire manual.",
            "Sub-Cmds": [set_vars, "commands"],
            "Usage": "help, help <command>, help <variable>",
            "Alias": "?"
        },
        "version": {
            "Command": "version",
            "Help": "Print the versioning information.",
            "Sub-Cmds": None,
            "Usage": "version",
            "Alias": None
        },
        "about": {
            "Command": "about",
            "Help": "Print the about information.",
            "Sub-Cmds": None,
            "Usage": "about",
            "Alias": None
        },
        "clear": {
            "Command": "clear",
            "Help": "Clear the screen.",
            "Sub-Cmds": None,
            "Usage": "clear",
            "Alias": "cls"
        },
        "use": {
            "Command": "use",
            "Help": "Load a new plugin.  This will add any new variables and erase all data associated to any previously loaded plugins.",
            "Sub-Cmds": avail_mods_to_list(),
            "Usage": "use <plugin>",
            "Alias": "load"
        },
        "reload": {
            "Command": "reload",
            "Help": "Reload the currently loaded plugin.  Helpful if you are troubleshooting the plugin or modifying it.",
            "Sub-Cmds": [get_loaded_plugin_name()],
            "Usage": "clear",
            "Alias": None
        },
        "set": {
            "Command": "set",
            "Help": "Load a parameter to a given variable.",
            "Sub-Cmds": set_vars,
            "Usage": "set <variable>",
            "Alias": None
        },
        "unset": {
            "Command": "unset",
            "Help": "Reset a variable to its default setting.",
            "Sub-Cmds": set_vars,
            "Usage": "unset <variable>",
            "Alias": None
        },
        "back": {
            "Command": "back",
            "Help": "'Go back' and remove the loaded plugin.",
            "Sub-Cmds": None,
            "Usage": "back",
            "Alias": None
        },
        "run": {
            "Command": "run",
            "Help": "Execute the bruteforce method through the plugin's 'run' function.",
            "Sub-Cmds": None,
            "Usage": "unset <variable>",
            "Alias": "broot"
        },
        "save": {
            "Command": "save",
            "Help": "Save either the configuration's sequence (config) or the framework's state (state).  Saving the 'state' will save the state of all variables.",
            "Sub-Cmds": ["state", "config"],
            "Usage": "save <sub-cmd>",
            "Alias": None
        },
        "validate": {
            "Command": "validate",
            "Help": "Do a quick check for a loaded plugin, target, username, and password.  This is run before every 'run' command.",
            "Sub-Cmds": None,
            "Usage": "validate",
            "Alias": None
        },
        "exit": {
            "Command": "exit",
            "Help": "Exit the program.",
            "Sub-Cmds": None,
            "Usage": "exit",
            "Alias": ["x", "quit", "q"]
        },
    }