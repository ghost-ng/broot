import sys, os
import var, save
import multiprocessing
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
from printlib import *
import threading
from time import sleep
import queue
import scan

loaded_plugin = var.get_loaded_plugin_object()
exitFlag = False
queueLock = threading.Lock()
task_queue = queue.Queue(10)
attempt_number = 1
threads = []
offline_hosts = []
online_hosts = []

verbose = var.global_vars['verbose']['Value']

#Order of checks
# passwords
#     a. password file
#     b. password list
#     c. single password
# usernames
#     a. username file
#     b. username list
#     c. single username
# targets
#     a. target file
#     b. target list
#     c. single target

def clear_screen():
    #os.system('cls' if os.name == 'nt' else 'clear')
    pass

def file_exists(filename):
    exists = os.path.isfile(filename)  # initial check   
    while exists is False:
        print_fail("File does not exist, try again")
        file = input("[New File]: ")
        return file_exists(file)
    return exists

def get_passwords():
    password_list = ""
    if var.global_vars['password-file']['Value'] is not None:
        password_list = open(var.global_vars['password-file']['Value'],'r')
    elif var.global_vars['password-list']['Value'] is not None:
        password_list = var.global_vars['password-list']['Value']
    else:
        password_list = [var.global_vars['password']['Value']]
    return password_list

def get_usernames():
    username_list = ""
    if var.global_vars['username-file']['Value'] is not None:
        username_list = open(var.global_vars['username-file']['Value'],'r')
    elif var.global_vars['usernames']['Value'] is not None:
        username_list = var.global_vars['usernames']['Value']
        username_list = username_list.split(",")

    else:
        username_list = [var.global_vars['username']['Value']]
    return username_list

def get_targets():
    target_list = ""
    if var.global_vars['target-file']['Value'] is not None:
        target_list = open(var.global_vars['target-file']['Value'],'r')
    elif var.global_vars['targets']['Value'] is not None:
        targets = var.global_vars['targets']['Value']
        target_list = targets.split(",")

    else:
        target_list = [var.global_vars['target']['Value']]
    return target_list

def clean_up(obj):
    if type(obj) is not list:
        obj.close()

def check_status(status, creds):
    target, username, password = creds
    target = get_target(target)
    port = get_port(target)
    plugin_name = var.get_loaded_plugin_name()
    attempt = "Plugin:{} Target:{}:{} Username:{} Password:{}".format(plugin_name, target, port, username, password)
    if status is True:
        print_good("Success --> {}".format(attempt))
        var.save_creds(creds)
        save.save_credentials(attempt)
    elif status is False:
        if target not in offline_hosts:
            if var.global_vars['print-failures']['Value'] is True or verbose is True:
                print_fail("Failed --> {}".format(attempt))

class brootThread (threading.Thread):

    def __init__(self, thread_id, q, loaded_plugin):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.q = q
        self.loaded_plugin = loaded_plugin

    def run(self):
        if verbose:
            print("running thread", self.thread_id)
        broot(self.q, self.loaded_plugin)

def broot(q, loaded_plugin):
    global attempt_number
    global offline_hosts
    global online_hosts
    global exitFlag

    wait_interval = var.global_vars['wait-interval']['Value']
    if wait_interval == 0:
        wait_interval = 1
    wait_time = var.global_vars['wait-time']['Value']
    wait_failure = var.global_vars['wait-on-failure']['Value']
    re_try = var.global_vars['re-try']['Value']
    stop = var.global_vars['stop-on-success']['Value']
    skip = False

    exitFlag = False

    attempt_number = 0
    while not exitFlag:
        if "random" in str(var.global_vars['wait-interval']['Value']):
            temp = var.global_vars['wait-interval']['Value']
            wait_interval = var.gen_random(temp)
        if "random" in str(var.global_vars['wait-time']['Value']):
            temp = var.global_vars['wait-time']['Value']
            wait_time = var.gen_random(temp)
        if "random" in str(var.global_vars['wait-on-failure']['Value']):
            temp = var.global_vars['wait-on-failure']['Value']
            wait_failure = var.gen_random(temp)
        if "random" in str(var.global_vars['re-try']['Value']):
            temp = var.global_vars['re-try']['Value']
            re_try = var.gen_random(temp)
        if not task_queue.empty():
            creds = q.get()
            target, username, password = creds
            target = get_target(target)
            port = get_port(target)
            attempt = "Target:{}:{} Username:{} Password:{}".format(target, port, username, password)
            
            if attempt_number % wait_interval == 0 and attempt_number > 0:
                if verbose:
                    print("[wait-interval] Sleeping for {} sec".format(wait_time))
                sleep(wait_time)
            if "username" in str(stop) and username in str(var.system_vars['valid-creds']['Usernames']):
                skip = True
                if verbose:
                    print_info("Creds already found for this username, skipping...")
            if "target" in str(stop) and target in str(var.system_vars['valid-creds']['Targets']):
                skip = True
                if verbose:
                    print_info("Creds already found for this target, skipping...")

            if skip is False:
                try:
                    if var.global_vars['probe-first']['Value'] is True and target not in offline_hosts:
                        if target not in online_hosts:
                            probe_status = scan.scan_port(port, target)
                            if probe_status is True:
                                online_hosts.append(target)
                        
                        if probe_status is True:
                            if verbose:
                                print_good("Target service is responsive!")
                        else:
                            offline_hosts.append(target)
                            if verbose:
                                print_warn("Target service did not respond!")
                except Exception as e:
                    if verbose:
                        print(e)
                        print(sys.exc_info)
                try:
                    if target not in offline_hosts:
                        print_info("Trying --> {}".format(attempt))
                        status = loaded_plugin.run(username, password, target, port)
                    elif target in offline_hosts:
                        status = False
                        if verbose:
                            print_info("Target previously observed offline")
                except NameError as e:
                    if verbose:
                        print(e)
                        print(sys.exc_info)
                    if "run" in str(e):
                        print_fail("Unable to find the mandatory 'run' function")
                    return
                check_status(status, creds)
                attempt_number += 1

                if status is False and wait_failure > 0:
                    if verbose:
                        print("[failed] Sleeping for {} sec".format(wait_failure))
                    sleep(wait_failure)
                if status is False and re_try > 0:
                    if verbose:
                        print("Trying again...")
                    for i in range(re_try):
                        if status is False:
                            if attempt_number % wait_interval == 0 and attempt_number > 0:
                                if verbose:
                                    print("[re-try,wait-interval] Sleeping for {} sec".format(wait_time))
                                sleep(wait_time)
                            try:
                                status = loaded_plugin.run(username, password, target, port)
                            except NameError:
                                print_fail("Unable to find 'run' function")
                                return
                            check_status(status, creds)
                            attempt_number += 1
                
            else:
                if verbose:
                    print("Skipping...")
                attempt_number += 1
            
        else:
            #print("queue is empty")
            #queueLock.release()
            #exitFlag = True
            sleep(.5)

def get_port(text):
    temp = text.split(":")
    if len(temp) > 1:
        return temp[1]
    else:
        return var.global_vars['target-port']['Value']

def get_target(text):
    temp = text.split(":")
    if len(temp) > 1:
        return temp[0]
    else:
        return text

def kill_threads(threads):
    global exitFlag
    exitFlag = True
    # Wait for all threads to complete
    for t in threads:
        t.join()
    print ("All Done!")

def initialize():
    global exitFlag
    global threads
    threads_input = var.global_vars['threads']['Value']
    if "random" in str(threads_input):
        num_threads = var.gen_random(threads_input)
    else:
        num_threads = int(var.global_vars['threads']['Value'])
    threads = []
    loaded_plugin = var.get_loaded_plugin_object()
    for x in range(num_threads):
        # Create new threads
        thread = brootThread(x, task_queue, loaded_plugin)
        thread.start()
        threads.append(thread)
    try:
#        print(loaded_plugin)
        target_list = get_targets()
        username_list = get_usernames()
        password_list = get_passwords()
    except KeyboardInterrupt:
        print("punch!")
    except Exception as e:
        print(e)
        print("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))

    try:
        #Load the queue
        #queueLock.acquire()
        for target in target_list:
            #print_info("Current Target: " + target)
            for username in username_list:
                #print_info("Current Username: " + username)
                #if type(username_list) is not list:
                    #username_list.seek(0)
                for password in password_list:
                    task_queue.put((target.rstrip(), username.rstrip(), password.rstrip()))
                if type(password_list) is not list:
                    password_list.seek(0)
            if type(username_list) is not list:
                    username_list.seek(0)
        #queueLock.release()
    except KeyboardInterrupt:
        print("punch!")
    except Exception as e:
        print(e)
        print("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
    
    try:
        clean_up(target_list)
        clean_up(password_list)
        clean_up(target_list)
    except KeyboardInterrupt:
        print("punch!")
    except UnboundLocalError as e:
        if verbose:
            print(e)
            print(sys.exc_info)
    try:
        # Wait for queue to empty
        while not task_queue.empty():
            pass
        # Notify threads it's time to exit
        exitFlag = True
        # Wait for all threads to complete
        for t in threads:
            t.join()
        print ("All Done!")
    except KeyboardInterrupt:
        exitFlag = True
        print("punch!")
    except Exception as e:
        print(e)
        print("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))

if __name__ == "__main__":
    initialize()