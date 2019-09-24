import os
import sys
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
from printlib import *
import var
from prettytable import PrettyTable
import datetime

def init():
    config_file = os.path.join(os.getcwd(), "..", "saves", "configs.txt")
    save_file = os.path.join(os.getcwd(), "..", "saves", "creds.txt")
    if os.path.isfile(config_file) is False:
        with open(config_file, 'a', encoding='utf-8') as file:
            pass
    if os.path.isfile(save_file) is False:
        with open(save_file, 'a', encoding='utf-8')as file:
            pass

def get_current_sequence():
    sequence = "seq="
    for item in var.global_vars:
        if var.global_vars[item]['Value'] != var.global_vars[item]['Default']:
            value = var.global_vars[item]['Value']
            command = "set " + item + " " + str(value) + ";"
            sequence = sequence + command
    
    if var.check_plugin_loaded():
        mod_name = var.get_loaded_plugin_name()
        command = "load " + mod_name + ";"
        sequence = sequence + command
        loaded_plugin = var.get_loaded_plugin_object()
        for item in loaded_plugin.plugin_vars:
            if loaded_plugin.plugin_vars[item]['Value'] != loaded_plugin.plugin_vars[item]['Default']:
                value = loaded_plugin.plugin_vars[item]['Value']
                command = "set " + item + " " + str(value) + ";"
                sequence = sequence + command
    return sequence

def export_sequence(filename):
    save_file = "../saves/configs.txt"
    with open(save_file, 'a') as file:
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
        if var.global_vars['verbose']['Value'] is True:
            print(e)
            print(sys.exc_info())


def show_sequences():
    import_file = "../saves/configs.txt"
    table = PrettyTable(['ID', 'Date', 'Sequence'])
    table.title = "Saved Configs"
    with open(import_file, 'r') as file:
        temp = []
        count = 0
        for line in file:
            temp = line.split("||")
            count += 1
            table.add_row([count, temp[0], temp[1]])
    print(table)

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