import sys, os
import var, save
import multiprocessing
from printlib import *
import threading
from time import sleep
import queue
import scan
MODULE_NAME = __file__.split("/")[len(__file__.split("/"))-1]

loaded_plugin = var.get_loaded_plugin_object()
exitFlag = False
queueLock = threading.Lock()
task_queue = queue.Queue(10)
attempt_number = 1
threads = []
offline_hosts = []
online_hosts = []

REASON_TO_SKIP = ""

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

def check_to_skip(target, username):
    global REASON_TO_SKIP
    skip = False
    if 'target' in var.global_vars['stop-on-success']['Value'] and target in var.system_vars["valid-creds"]['Targets']:
        skip = True
        REASON_TO_SKIP = 'Creds Found for This Target'
    if 'username' in var.global_vars['stop-on-success']['Value'] and username in var.system_vars["valid-creds"]['Usernames']:
        skip = True
        REASON_TO_SKIP = 'Creds Found for This Username'
    return skip

def clean_up(obj):
    if type(obj) is not list:
        obj.close()


def check_status(status, creds):
    global exitFlag
    verbose = var.global_vars['verbose']['Value']
    target, username, password = creds
    target = get_target(target)
    port = get_port(target)
    plugin_name = var.get_loaded_plugin_name()
    if port is None:
        attempt = "Plugin:{} Target:{} Username:{} Password:{}".format(plugin_name, target, username, password)
    else:
        attempt = "Plugin:{} Target:{}:{} Username:{} Password:{}".format(plugin_name, target, port, username, password)
    if status is True:
        if var.global_vars['print-successes']['Value'] or verbose:
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
        verbose = var.global_vars['verbose']['Value']
        if verbose:
            print_info("Running Thread {}".format(self.thread_id))
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
    syn_probe = var.global_vars['syn-probe']['Value']
    tcp_probe = var.global_vars['tcp-probe']['Value']
    verbose = var.global_vars['verbose']['Value']
    offline = False
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
            target = target.rstrip()
            username = username.rstrip()
            password = password.rstrip()
            target = get_target(target)
            skip = check_to_skip(target, username)
            port = get_port(target)
            attempt = "Target:{}:{} Username:{} Password:{}".format(target, port, username, password)
            
            if skip is False:
                if attempt_number % wait_interval == 0 and attempt_number > 0:
                    if verbose:
                        print("[wait-interval] Sleeping for {} sec".format(wait_time))
                    sleep(wait_time)

            if skip is False:
                if var.global_vars['syn-probe']['Value'] is True or var.global_vars['tcp-probe']['Value'] is True:
                    probe = True
                else:
                    probe = False
                if probe is True and ((target,port) not in online_hosts and (target,port) not in offline_hosts):        #check it wasnt previously scanned
                    if var.global_vars['syn-probe']['Value'] is True:
                        #try:
                        probe_status = scan.send_syn_probe(port, target)
                        # except Exception as e:
                        #     if verbose:
                        #         print(e)
                        #         print(sys.exc_info)
                        #         print("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
                    elif var.global_vars['tcp-probe']['Value'] is True:
                        #try:
                        probe_status = scan.send_tcp_probe(port, target)
                        # except Exception as e:
                        #     if verbose:
                        #         print(e)
                        #         print(sys.exc_info)
                        #         print("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
                    if probe_status is True:
                        online_hosts.append((target,port))
                        if verbose:
                            print_good("Target service is responsive!")                            
                    else:
                        offline_hosts.append((target,port))
                        if verbose:
                            print_warn("Target service did not respond!")
        
                    if (target,port) not in offline_hosts:
                        if verbose or var.global_vars['print-attempts']['Value']:
                            print_info("Trying --> {}".format(attempt))
                        try:
                            status = loaded_plugin.run(username, password, target, port)    #RETURN: True --> successful login; False --> Login failed; None --> login attempt skipped
                        except Exception as e:
                            if verbose:
                                print_fail(str(e))
                                print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
                                print_fail("Error in Module - {}".format(MODULE_NAME))
                    elif (target,port) in offline_hosts:
                        status = False
                        if verbose:
                            print_info("Skipping, {}:{} observed offline".format(target, port))
                            offline = True
                else:
                    if verbose or var.global_vars['print-attempts']['Value']:
                        print_info("Trying --> {}".format(attempt))
                    try:   
                        status = loaded_plugin.run(username, password, target, port)        #RETURN: True --> successful login; False --> Login failed; None --> login attempt skipped
                    except Exception as e:
                        if verbose:
                            print_fail(str(e))
                            print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
                            print_fail("Error in Module - {}".format(MODULE_NAME))
                        if "run" in str(e):
                            print_fail("Unable to find the mandatory 'run' function")
                        return
                if offline is False and status is not None:
                    check_status(status, creds)
                    attempt_number += 1

                if status is False and wait_failure > 0 and status is not None:
                    if verbose:
                        print("[failed] Sleeping for {} sec".format(wait_failure))
                    sleep(wait_failure)
                if status is False and re_try > 0 and status is not None:
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
                            except Exception as e:
                                if verbose:
                                    print_fail(str(e))
                                    print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
                                    print_fail("Error in Module - {}".format(MODULE_NAME))
                            check_status(status, creds)
                            attempt_number += 1
                
            else:
                pass
            
        else:
            #print("queue is empty")
            #queueLock.release()
            #exitFlag = True
            sleep(.5)

def get_port(text):
    if var.global_vars['target-port']['Value'] is not None:    
        temp = text.split(":")
        if len(temp) > 1:
            return temp[1]
        else:
            return var.global_vars['target-port']['Value']
    else:
        return None

def get_target(text):
    if "http" not in text:
        temp = text.split(":")
        if len(temp) > 1:
            return temp[0]
        else:
            return text
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
    verbose = var.global_vars['verbose']['Value']

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
        if verbose:
            print_fail(str(e))
            print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
            print_fail("Error in Module - {}".format(MODULE_NAME))

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
        if verbose:
            print_fail(str(e))
            print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
            print_fail("Error in Module - {}".format(MODULE_NAME))
    
    try:
        clean_up(target_list)
        clean_up(password_list)
        clean_up(target_list)
    except KeyboardInterrupt:
        print("punch!")
    except UnboundLocalError as e:
        if verbose:
            print_fail(str(e))
            print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
            print_fail("Error in Module - {}".format(MODULE_NAME))
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
        if verbose:
            print_fail(str(e))
            print_fail("Error on Line:{}".format(sys.exc_info()[-1].tb_lineno))
            print_fail("Error in Module - {}".format(MODULE_NAME))

if __name__ == "__main__":
    initialize()