import os
import sys
sys.path.append(os.getcwd() + "\\..\\misc")
import colors
import var

def get_current_sequence():
    sequence = "seq="
    for item in var.global_vars:
        value = var.global_vars[item]['Value']
        command = "set " + item + " " + str(value) + ";"
        sequence = sequence + command
    
    if var.check_module_loaded():
        mod_name = var.get_loaded_module_name()
        command = "load " + mod_name + ";"
        sequence = sequence + command
        loaded_module = var.get_loaded_module_object()
        for item in loaded_module.module_vars:
            value = loaded_module.module_vars[item]['Value']
            command = "set " + item + " " + str(value) + ";"
            sequence = sequence + command
    return sequence

def export_sequence():
    save_file = "../saves/saves.txt"
    with open(save_file,'a') as file:
        seq = get_current_sequence()
        file.write(seq+"\n")
    colors.PrintColor("SUCCESS","Saved Current Sequence")