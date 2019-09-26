import sys
import os
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
from printlib import *
import var


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
#CHECK IF TARGET-PORT IS SET
    if not isinstance(var.global_vars['target-port']['Value'], int):
        print_warn("You may need to specify a target-port")
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