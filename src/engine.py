import sys, os
import var
import multiprocessing
sys.path.append(os.getcwd() + "\\..\\misc")
import colors
import threading
from time import sleep
import queue

loaded_module = var.get_loaded_module_object()
exitFlag = 0
queueLock = threading.Lock()
task_queue = queue.Queue(10)
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
    return exists

def get_passwords():
    if var.global_vars['password-file']['Value'] is not None:
        file_exists(var.global_vars['password-file']['Value'])
        password_list = open(var.global_vars['password-file']['Value'],'r')
    else:
        password_list = [var.global_vars['password']['Value']]
    return password_list

def get_usernames():
    if var.global_vars['username-file']['Value'] is not None:
        file_exists(var.global_vars['username-file']['Value'])
        username_list = open(var.global_vars['username-file']['Value'],'r')
    else:
        username_list = [var.global_vars['username']['Value']]
    return username_list

def get_targets():
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

class brootThread (threading.Thread):
    def __init__(self, x, q, loaded_module):
        threading.Thread.__init__(self)
        self.thread_id = x
        self.q = q
        self.loaded_module = loaded_module
    def run(self):
        print("running thread",self.thread_id)
        broot(self.q, self.loaded_module)

def broot(q, loaded_module):
    while not exitFlag:
        #queueLock.acquire()
        if not task_queue.empty(): 
            target, username, password = q.get()
            #queueLock.release()
            loaded_module.run(username, password, target)
        else:
            #queueLock.release()
            sleep(.5)

def initialize():
    global exitFlag

    num_threads = int(var.global_vars['threads']['Value'])
    threads = []
    loaded_module = var.get_loaded_module_object()
    for x in range(num_threads):
        # Create new threads
        thread = brootThread(x, task_queue, loaded_module)
        thread.start()
        threads.append(thread)
    try:
#        print(loaded_module)
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
                for password in password_list:
                    task_queue.put((target, username, password))
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
    try:
        # Wait for queue to empty
        while not task_queue.empty():
            pass
        # Notify threads it's time to exit
        exitFlag = 1
        # Wait for all threads to complete
        for t in threads:
            t.join()
        print ("All Done!")
    except KeyboardInterrupt:
        print("punch!")
    except Exception as e:
        print(e)  

if __name__ == "__main__":
    initialize()