print("Loading...")
import os, sys, signal
from time import sleep
import var
import engine
sys.path.append(os.getcwd() + "\\..\\misc")
import colors
import importlib
import art
import export

module = "/broot"
prompt = module + "/>> "
end_prgm_flag = False
version = "broot v" + str(.90)
about = """
Author: midnightseer
About: 
    broot is a crowdsourced open source bruteforcing framework."""

def update_paths():
    dir_list = next(os.walk('..//modules'))[1]
    for path in dir_list:
        sys.path.append(os.getcwd() + "\\..\\modules\\" + path)

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
    global module
    avail_cmds = []
    exit_cmds = ["quit", "exit", "q", "x"]
    verbose = var.global_vars['verbose']['Value']
    for i in var.global_cmds.keys(): avail_cmds.append(i)
    if var.check_module_loaded():
        loaded_module = var.get_loaded_module_object()
        for i in loaded_module.module_cmds.keys(): avail_cmds.append(i)
    try:
        if cmds[0] in avail_cmds:
            if cmds[0] in exit_cmds:
                colors.PrintColor("INFO", "Exiting")
                engine.exitFlag = True
                sys.exit()
            elif cmds[0] == "validate":
                if validate_options() is True:
                    colors.PrintColor("INFO", "Everything seems ok!")
            elif cmds[0] in ['clear', 'cls']:
                clear_screen()
            elif cmds[0] == "version":
                print(version)
            elif cmds[0] == "about":
                print(about)
            elif cmds[0] == "help" or cmds[0] == "?":
                if len(cmds) > 1:
                    try:
                        if cmds[1] in var.global_vars:
                            var.print_enum_dict(var.global_vars[cmds[1]], m="vars")
                            print()
                        elif var.check_module_loaded():
                            loaded_module = var.get_loaded_module_object()
                            if cmds[1] in loaded_module.module_vars:
                                var.print_enum_dict(loaded_module.module_vars[cmds[1]], m="vars")
                            print()
                        else:
                            print("Help topic does not exist!")
                    except Exception as e:
                        print("Error in looking up help entry!")
                        if verbose:
                            print(e)
                else:
                    var.print_enum_dict(var.global_vars, m="vars")
                    if var.check_module_loaded():
                        loaded_module = var.get_loaded_module_object()
                        print()
                        print("*** Module Commands ***")
                        var.print_enum_dict(loaded_module.module_vars, m="vars")
            elif cmds[0] == "run" or cmds[0] == "broot":
                if validate_options() is True:
                    colors.PrintColor("INFO", "Executing...")
                    if var.check_module_loaded():
                        engine.initialize()
                    importlib.reload(engine)
            elif cmds[0] == "back":
                module = "/broot"
                var.unload_module()
                var.wipe_loaded_module_info()
            elif cmds[0] == "reload":
                if cmds[1] == var.get_loaded_module_name():
                    var.reload_loaded_module()
                if cmds[1] == "modules":
                    var.refresh_modules()
                    var.count_modules()
                #if cmds[1] == "self":
                #    importlib.reload(engine)
                #    importlib.reload(var)
            elif cmds[0] == "save":
                if cmds[1] == "sequence":
                    export.export_sequence()
            elif cmds[0] == "show":
                if cmds[1] in ['seq', 'sequence']:
                    seq = export.get_current_sequence()
                    print(seq)
                if cmds[1] == "creds":
                    var.print_successes()
                if cmds[1] == "modules":
                    var.show_modules()
                if cmds[1] == "commands":
                    var.refresh_modules()
                    var.print_enum_dict(var.global_cmds, m="tree")
                    if var.check_module_loaded():
                        loaded_module_name = var.get_loaded_module_name()
                        loaded_module_object = var.get_loaded_module_object()
                        print("New Available Commands for '{}' Module:".format(loaded_module_name))
                        var.print_enum_dict(loaded_module_object.module_cmds, m="tree")
                if cmds[1] == "loaded-module":
                    if len(cmds) > 2:
                        if cmds[2] == "name":
                            print(var.get_loaded_module_name())
                        if cmds[2] == "object":
                            print(var.get_loaded_module_object())
                if cmds[1] == "options":
                    var.opts_to_table("global")
                    if var.check_module_loaded():
                        var.opts_to_table("module")
            elif cmds[0] == "use" or cmds[0] == "load":
                try:
                    var.import_module(cmds[1])
                    colors.PrintColor("SUCCESS", "Loaded {} module successfully".format(cmds[1]))
                    module = module + "/" + cmds[1]
                    var.update_cmds()
                except ModuleNotFoundError as e:
                    colors.PrintColor("FAIL", "Module not found")
                except:
                    colors.PrintColor("FAIL", "Unable to load module")
                    print(sys.exc_info())
                
            elif cmds[0] == "set":
                if cmds[1] not in var.global_cmds['set']:
                    print("Command '" + cmds[1] + "' does not exist")
                else:
                    try:
                        loaded_module = var.get_loaded_module_object()
                        if cmds[1] in var.global_vars:
                            variable = var.global_vars[cmds[1].lower()]
                            if cmds[2] == 'random':
                                handle_random_input(variable, cmds)
                            else:
                                variable['Value'] = format_variable(variable, cmds[2])
                        elif cmds[1] in loaded_module.module_vars:
                            variable = loaded_module.module_vars[cmds[1].lower()]
                            variable['Value'] = format_variable(variable, cmds[2])
                    except Exception as e:
                        colors.PrintColor("FAIL", "Unable to set variable (is the right module loaded?)")
                        if verbose:
                            print(e)
            elif cmds[0] == "unset":
                if var.check_module_loaded():
                    loaded_module = var.get_loaded_module_object()
                try:
                    if cmds[1] in var.global_vars:
                        variable = var.global_vars[cmds[1]]
                        reset_value = variable['Default']
                        variable['Value'] = format_variable(variable, reset_value)
                    elif cmds[1] in loaded_module.module_vars:
                        variable = loaded_module.module_vars[cmds[1]]
                        reset_value = variable['Default']
                        variable['Value'] = format_variable(variable, reset_value)
                except Exception as e:
                    colors.PrintColor("FAIL", "Unable to reset the variable (are you sure that's the right variable?)")
                    if verbose:
                        print(e)
            if var.check_module_loaded():
                if cmds[0] == var.get_loaded_module_name():
                    loaded_module = var.get_loaded_module_object()
                    loaded_module.module_commands(cmds)
        else:
            print("Unrecognized Command -->", '"' + str(cmds) + '"')
    except IndexError:
        colors.PrintColor("FAIL", "Incomplete Command")

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
        colors.PrintColor("FAIL", "Please specify a username, usernames, or username file")
        validated = False
#CHECK PASSWORD OPTIONS
    if var.global_vars['password-file']['Value'] is None:
        pass_file = 0
    else:
        pass_file = 1
    if var.global_vars['password']['Value'] is None:
        password = 0
    else:
        password = 1
    if pass_file + password == 0:
        colors.PrintColor("FAIL", "Please specify a password or password file")
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
        colors.PrintColor("FAIL", "Please specify a target, targets, or target file")
        validated = False
#CHECK IF MODULE IS LOADED
    if var.check_module_loaded() is False:
        colors.PrintColor("FAIL", "Please load a module")
        validated = False
    return validated

def format_variable(variable, setting):
    bool_true = ["yes", "true", "1", "t"]
    bool_false = ["no", "false", "0", "n"]
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
            colors.PrintColor("FAIL", "Incorrect variable type")
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
        colors.PrintColor("WARN", "Cannot set a random value to a non-interger type")

def initialize():
    clear_screen()
    var.refresh_modules()
    update_paths()
    print(art.banner)
    print(about)
    print(version)

def main():
    initialize()
    while not end_prgm_flag:
        prompt = module + "/>> "
        response = input(prompt).lower()
        commands = response
        if "seq=" in response:
            temp = response.replace("seq=", '')
            commands = temp.rstrip(";").split(";")
            for cmd in commands:
                temp = cmd.split(" ")
                parse_cmds(temp)     
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