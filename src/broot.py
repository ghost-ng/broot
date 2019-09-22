print("Loading...")
import os, sys, signal
from time import sleep
import var
import engine
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
from printlib import *
import importlib
import art
import save

plugin = "/broot"
prompt = plugin + "/>> "
end_prgm_flag = False
version = "broot v" + str(.90)
about = """
Author: midnightseer
About: 
    broot is a crowdsourced open source bruteforcing framework."""

def update_paths():
    dir_list = next(os.walk(os.path.join(os.getcwd(), "..", "plugins")))[1]
    for path in dir_list:
        sys.path.append(os.path.join(os.path.join(os.getcwd(), "..", "plugins"), path))

def signal_handler(signal, frame):
    global end_prgm_flag
    print("punt!")
    end_prgm_flag = True
    sys.exit(0)

#signal.signal(signal.SIGINT, signal_handler)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    pass

def parse_cmds(cmds):
    global prompt
    global plugin
    avail_cmds = var.get_available_cmds()
    #print(avail_cmds)
    exit_cmds = ["exit"] + var.global_cmds['exit']['Alias']
    #print(exit_cmds)
    verbose = var.global_vars['verbose']['Value']
    try:
        if cmds[0].lower() in avail_cmds:
            if cmds[0].lower() in exit_cmds:
                print_info("Exiting")
                engine.exitFlag = True
                sys.exit()
            elif cmds[0].lower() == "reset":
                if len(cmds) > 1:
                    if cmds[1].lower() == "creds":
                        creds = var.system_vars['valid-creds']
                        creds['Credentials'] = []
                        creds['Usernames'] = []
                        creds['Targets'] = []
                else:
                    var.reset_all_vars()
                    print_info("Reset complete")
            elif cmds[0].lower() == "validate":
                try:
                    if validate_options() is True:
                        print_info("Everything seems ok!")
                    else:
                        print_fail("Validation Failed!")
                except Exception as e:
                    print_fail("Error")
                    if verbose:
                        print(e)
                        print(sys.exc_info)
            elif cmds[0].lower() in ['clear', 'cls']:
                clear_screen()
            elif cmds[0].lower() == "version":
                print(version)
            elif cmds[0].lower() == "about":
                print(about)
            elif cmds[0].lower() == "help" or cmds[0] == "?":
                var.get_help(cmds)
            elif cmds[0].lower() == "run" or cmds[0].lower() == "broot":
                if validate_options() is True:
                    print_info("Executing...")
                    if var.check_plugin_loaded():
                        engine.initialize()
                    importlib.reload(engine)
                else:
                    print_fail("Validation Failed!")
            elif cmds[0].lower() == "back":
                plugin = "/broot"
                var.unload_plugin()
                var.wipe_loaded_plugin_info()
            elif cmds[0].lower() == "reload":
                if cmds[1].lower() == var.get_loaded_plugin_name():
                    var.reload_loaded_plugin()
                if cmds[1].lower() == "plugins":
                    var.refresh_plugins()
                    var.show_plugins()
                    var.count_plugins()
                    var.update_cmds()
                #if cmds[1].lower() == "self":
                #    importlib.reload(engine)
                #    importlib.reload(var)
            elif cmds[0].lower() == "save":
                if cmds[1].lower() == "config":
                    save.export_sequence()
            elif cmds[0].lower() == "show":
                if cmds[1].lower() == 'config':
                    seq = save.get_current_sequence()
                    print(seq)
                if cmds[1].lower() == 'saved-configs':
                    save.show_sequences()
                if cmds[1].lower() == "creds":
                    var.print_successes()
                if cmds[1].lower() == "plugins":
                    #var.refresh_plugins()
                    var.show_plugins()
                    #var.count_plugins()
                if cmds[1].lower() == "commands":
                    var.refresh_plugins()
                    var.print_cmds(var.global_cmds)
                    #var.print_enum_dict(var.global_cmds, m="tree")
                    if var.check_plugin_loaded():
                        loaded_plugin_name = var.get_loaded_plugin_name()
                        loaded_plugin_object = var.get_loaded_plugin_object()
                        print_info("New Available Commands for '{}' Plugin:\n".format(loaded_plugin_name))
                        var.print_cmds(loaded_plugin_object.plugin_cmds)
                if cmds[1].lower() == "sub-cmds":
                    if len(cmds) == 3:
                        sub_cmds = var.get_sub_cmds(cmds[2])
                        try:
                            for x in sub_cmds: print(x)
                        except TypeError:
                            pass
                if cmds[1].lower() == "loaded-plugin":
                    if len(cmds) > 2:
                        if cmds[2] == "name":
                            print(var.get_loaded_plugin_name())
                        if cmds[2] == "object":
                            print(var.get_loaded_plugin_object())
                if cmds[1].lower() == "options":
                    var.opts_to_table("global")
                    if var.check_plugin_loaded():
                        var.opts_to_table("plugin")
            elif cmds[0].lower() == "use" or cmds[0].lower() == "load":
                if cmds[1].lower() == "config":
                    try:
                        resp = input("[?] [m]erge/[r]eset: ")
                        if resp.lower() == "r":
                            var.reset_all_vars()
                        seq = save.load_sequences(cmds[2])
                        parse_seq(seq.rstrip())
                    except IndexError:
                        pass
                else:
                    try:
                        var.import_plugin(cmds[1].lower())
                        print_good("Loaded {} plugin successfully".format(cmds[1].lower()))
                        if cmds[1].lower() not in plugin:
                            plugin = plugin + "/" + cmds[1].lower()
                        var.update_cmds()
                    except ModuleNotFoundError as e:
                        print_fail("Plugin not found")
                    except:
                        print_fail("Unable to load plugin")
                        print(sys.exc_info())
                        print("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
                
            elif cmds[0].lower() == "set":
                if cmds[1].lower() not in var.global_cmds['set']['Sub-Cmds']:
                    print("Command '" + cmds[1] + "' does not exist")
                else:
                    try:
                        loaded_plugin = var.get_loaded_plugin_object()
                        if cmds[1].lower() in var.global_vars:
                            variable = var.global_vars[cmds[1].lower()]
                            if cmds[2].lower() == 'random':
                                handle_random_input(variable, cmds)
                            elif "file" in cmds[1].lower():
                                filename = var.file_exists(cmds[2])
                                variable['Value'] = filename
                            elif "list" in cmds[1].lower():
                                variable['Value'] = format_variable(variable)
                            else:
                                variable['Value'] = format_variable(variable, cmds[2])
                        elif cmds[1].lower() in loaded_plugin.plugin_vars:
                            variable = loaded_plugin.plugin_vars[cmds[1].lower()]
                            variable['Value'] = format_variable(variable, cmds[2])
                    except IndexError:
                        pass
                    except Exception as e:
                        print_fail("Unable to set variable (is the right plugin loaded?)")
                        if verbose:
                            print(e)
                            print("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
            elif cmds[0].lower() == "unset":
                if var.check_plugin_loaded():
                    loaded_plugin = var.get_loaded_plugin_object()
                try:
                    if cmds[1].lower() in var.global_vars:
                        variable = var.global_vars[cmds[1].lower()]
                        reset_value = variable['Default']
                        variable['Value'] = format_variable(variable, reset_value)
                    elif cmds[1].lower() in loaded_plugin.plugin_vars:
                        variable = loaded_plugin.plugin_vars[cmds[1].lower()]
                        reset_value = variable['Default']
                        variable['Value'] = format_variable(variable, reset_value)
                except Exception as e:
                    print_fail("Unable to reset the variable (are you sure that's the right variable?)")
                    if verbose:
                        print(e)
                        print("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
            if var.check_plugin_loaded():
                loaded_plugin = var.get_loaded_plugin_object()
                if cmds[0].lower() in loaded_plugin.plugin_cmds:
                    loaded_plugin.parse_plugin_cmds(cmds)
        else:
            print("Unrecognized Command -->", str(cmds))
    except IndexError:
        print_fail("Incomplete Command")

def validate_options():
    validated = True
#CHECK USERNAME OPTIONS
    if var.global_vars['username-file']['Value'] is None:
        user_file = 0
    else:
        user_file = 1
    if var.global_vars['usernames']['Value'] is None:
        users = 0
    else:
        users = 1
    if var.global_vars['username']['Value'] is None:
        user = 0
    else:
        user = 1
    if user_file + users + user == 0:
        print_fail("Please specify a username, usernames, or username file")
        validated = False
#CHECK PASSWORD OPTIONS
    if var.global_vars['password-file']['Value'] is None:
        pass_file = 0
    else:
        pass_file = 1
    if var.global_vars['password-list']['Value'] is None:
        password_list = 0
    else:
        password_list = 1
    if var.global_vars['password']['Value'] is None:
        password = 0
    else:
        password = 1
    if pass_file + password_list + password == 0:
        print_fail("Please specify a password, password list, or password file")
        validated = False
#CHECK TARGET OPTIONS
    if var.global_vars['target-file']['Value'] is None:
        target_file = 0
    else:
        target_file = 1
    if var.global_vars['targets']['Value'] is None:
        targets = 0
    else:
        targets = 1
    if var.global_vars['target']['Value'] is None:
        target = 0
    else:
        target = 1
    if target_file + targets + target == 0:
        print_fail("Please specify a target, targets, or target file")
        validated = False
#CHECK IF MODULE IS LOADED
    if var.check_plugin_loaded() is False:
        print_fail("Please load a plugin")
        validated = False
#VALIDATE MODULE STUFF
    else:
        loaded_plugin = var.get_loaded_plugin_object()
        if loaded_plugin.validate() is False:
            validated = False
    return validated

def format_variable(variable, setting=None):
    bool_true = ["yes", "true", "1", "t", "y"]
    bool_false = ["no", "false", "0", "n", "f"]
    if variable['Type'] == "Boolean":
        if str(setting).lower() in bool_true:
            return True
        elif str(setting).lower() in bool_false:
            return False
    elif variable['Type'] == 'Integer' and not "random" in str(setting):
        try:
            temp = int(setting)
            return temp
        except:
            print_fail("Incorrect variable type")
    elif variable['Type'] == 'List':
        exit_loop = False
        input_list = []
        print("Enter input, separate each item with ENTER [CTRL-C TO END]")
        while exit_loop is False:
            try:
                res = input()
                input_list.append(res)
            except KeyboardInterrupt:
                exit_loop = True
        return input_list

    elif str(setting).lower() == "none":
        return None
    else:
        return setting

def handle_random_input(variable, cmds):
    if variable['Type'] == "Integer":
        if len(cmds) == 4:
            new_cmd = cmds[2] + " " + cmds[3]
            variable['Value'] = format_variable(variable, new_cmd)
        else:
            variable['Value'] = format_variable(variable, cmds[2])
    else:
        print_warn("Cannot set a random value to a non-interger type")

def initialize():
    clear_screen()
    var.refresh_plugins()
    var.update_cmds()
    update_paths()
    print(art.banner)
    print(about)
    print(version)

def parse_seq(cmd):
    temp = cmd.replace("seq=", '')
    commands = temp.rstrip(";").split(";")
    for cmd in commands:
        temp = cmd.split(" ")
        parse_cmds(temp) 

def main():
    initialize()
    while not end_prgm_flag:
        prompt = plugin + "/>> "
        response = input(prompt)
        commands = response
        if "seq=" in response:
            parse_seq(response)    
        elif commands != "":
            cmds = commands.split(" ")
            parse_cmds(cmds)
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        #engine.kill_threads(engine.threads)
        engine.exitFlag = True
        print("punt!")