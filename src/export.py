import os
import sys
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
import colors
import var

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

def export_sequence():
    save_file = "../saves/saves.txt"
    with open(save_file,'a') as file:
        seq = get_current_sequence()
        file.write(seq)
        file.write('\n')
    colors.PrintColor("SUCCESS","Saved Current Sequence")