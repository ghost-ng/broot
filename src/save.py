import os
import sys
from printlib import *
import var
import datetime
MODULE_NAME = __file__.split("/")[len(__file__.split("/"))-1]

def init():
    config_file = os.path.join(os.getcwd(), "..", "saves", "configs.txt")
    cred_file = os.path.join(os.getcwd(), "..", "saves", "creds.txt")
    if os.path.isfile(config_file) is False:
        print_info("Creating a place to save configurations...")
        with open(config_file, 'a', encoding='utf-8'):
            pass
    if os.path.isfile(cred_file) is False:
        print_info("Creating a place to save credentials...")
        with open(cred_file, 'a', encoding='utf-8'):
            pass

def get_current_sequence():
    sequence = "seq="
    for item in var.global_vars:
        if var.global_vars[item]['Value'] != var.global_vars[item]['Default']:
            value = var.global_vars[item]['Value']
            command = "set " + item + " " + str(value) + "<|>"
            sequence = sequence + command
    
    if var.check_plugin_loaded():
        mod_name = var.get_loaded_plugin_name()
        command = "load " + mod_name + "<|>"
        sequence = sequence + command
        loaded_plugin = var.get_loaded_plugin_object()
        for item in loaded_plugin.plugin_vars:
            if loaded_plugin.plugin_vars[item]['Value'] != loaded_plugin.plugin_vars[item]['Default']:
                value = loaded_plugin.plugin_vars[item]['Value']
                command = "set " + item + " " + str(value) + "<|>"
                sequence = sequence + command
    return sequence

def export_sequence(filename="../saves/configs.txt"):
    with open(filename, 'a') as file:
        seq = get_current_sequence()
        dt = datetime.datetime.today().replace(second=0, microsecond=0)
        dt = str(dt).rstrip(':00')
        file.write(dt + "||" + seq)
        file.write('\n')
    print_good("Saved Current Sequence")

def save_credentials(creds, filename="../saves/creds.txt"):
    verbose = var.global_vars['verbose']['Value']
    try:
        with open(filename, 'a') as file:
            dt = datetime.datetime.today().replace(second=0, microsecond=0)
            dt = str(dt).rstrip(':00')
            line = "[{t}]:[{p}]::{c}".format(t=dt, p=var.get_loaded_plugin_name(), c=creds)
            file.write(line)
            file.write('\n')
        if verbose is True:
            print_good("Saved Credentials")
    except Exception as e:
        print_warn("Unable to save credentials")
        if verbose:
            print_fail(str(e))
            print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
            print_fail("Error in Module - {}".format(MODULE_NAME))


def show_sequences():
    import_file = "../saves/configs.txt"
    with open(import_file, 'r') as file:
        temp = []
        count = 0
        for line in file:
            temp = line.split("||")
            count += 1
            print("### SAVED-CONFIGS ###")
            print("ID: {}".format(count))
            print("SAVED ON: {}".format(temp[0]))
            print("SEQUENCE:")
            print(temp[1])
        if count == 0:
            print_info("There a no saved configs!")

def load_sequences(selection):
    selection = int(selection)
    import_file = "../saves/configs.txt"
    with open(import_file, 'r+',encoding='utf-8') as file:
        temp = []
        count = 1
        for line in file:
            temp = line.split("||")
            if selection == count:
                return temp[1]
            count += 1
        if selection > count:
            print_fail("Unable to load config; selection # does not exist")