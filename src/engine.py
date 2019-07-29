import sys, os
import var
import multiprocessing
sys.path.append(os.path.join(os.getcwd(), "..", "misc"))
import colors
import threading
from time import sleep
import queue

loaded_plugin = var.get_loaded_plugin_object()
exitFlag = False
queueLock = threading.Lock()
task_queue = queue.Queue(10)
attempt_number = 1
threads = []

#Order of checks
# passwords
#     a. password file
#     b. passwords list
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
    #colors.PrintColor("FAIL","File does not exist, try again")    
    while exists is False:
        colors.PrintColor("FAIL", "File does not exist, try again")
        file = input("[New File]: ")
        return file_exists(file)
    var.global_vars['password-file']['Value'] = file
    return exists

def get_passwords():
    password_list = ""
    if var.global_vars['password-file']['Value'] is not None:
        file_exists(var.global_vars['password-file']['Value'])
        password_list = open(var.global_vars['password-file']['Value'],'r')
    else:
        password_list = [var.global_vars['password']['Value']]
    return password_list

def get_usernames():
    username_list = ""
    if var.global_vars['username-file']['Value'] is not None:
        file_exists(var.global_vars['username-file']['Value'])
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
        file_exists(var.global_vars['target-file']['Value'])
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
    plugin_name = var.get_loaded_plugin_name()
    attempt = "Plugin:{} Target:{} Username:{} Password:{}".format(plugin_name, target, username, password)
    if status is True:
        colors.PrintColor("SUCCESS", "Success --> {}".format(attempt))
        var.save_creds(creds)
    elif status is False and var.global_vars['print-failures']['Value'] is True:
        colors.PrintColor("FAIL", "Failed --> {}".format(attempt))

class brootThread (threading.Thread):

    def __init__(self, thread_id, q, loaded_plugin):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.q = q
        self.loaded_plugin = loaded_plugin

    def run(self):
        if var.global_vars['verbose']['Value']:
            print("running thread", self.thread_id)
        broot(self.q, self.loaded_plugin)

def broot(q, loaded_plugin):
    global attempt_number
    global attempt_number
    global exitFlag

    verbose = var.global_vars['verbose']['Value']
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
            attempt = "Target:{} Username:{} Password:{}".format(target, username, password)
            
            if attempt_number % wait_interval == 0 and attempt_number > 0:
                if verbose:
                    print("[wait-interval] Sleeping for {} sec".format(wait_time))
                sleep(wait_time)
            if "username" in str(stop) and username in str(var.read_only_vars['valid-creds']['Usernames']):
                skip = True
            if "target" in str(stop) and target in str(var.read_only_vars['valid-creds']['Targets']):
                skip = True

            if skip is False:
                status = loaded_plugin.run(username, password, target)
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
                            success = loaded_plugin.run(username, password, target)
                            check_status(status, creds)
                            attempt_number += 1
            else:
                print("Skipping...")
                attempt_number += 1
            
        else:
            #print("queue is empty")
            #queueLock.release()
            #exitFlag = True
            sleep(.5)

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

    try:
        #Load the queue
        #queueLock.acquire()
        for target in target_list:
            #colors.PrintColor("INFO", "Current Target: " + target)
            for username in username_list:
                #colors.PrintColor("INFO", "Current Username: " + username)
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
    
    try:
        clean_up(target_list)
        clean_up(password_list)
        clean_up(target_list)
    except KeyboardInterrupt:
        print("punch!")
    except UnboundLocalError:
        pass
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

if __name__ == "__main__":
    initialize()