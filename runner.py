'''
AUTHOR: Tyler Gan
Date: 20/10/2020

This program runs RUNNER.PY. The purpose of this program is to run the Processes, using exec and fork, at its respective times.

The program imports from RUNNER_METHODS.PY and contains the following functions:
    1. receive_signal() - This receives the kill signal associated with the USR1 signal which will cause it to write the status of the program to the file, .runner-status, located
                          in the home directory.
        a. write_file() - works in conjunction with receive_signal() and is the function that writes to .runner-status.
    2. send_PID() - This function creates .runner-pid and writes this program's current PID to the file.
    3. create_statusf() - This function creates the status file, .runner-status and checks whether the file was successfully created.
    4. check_file() - This function works in conjucntion with send_PID() and create_statusf() to check whether the file has been created and has contents present in the file.
'''

import os, sys, datetime, time, signal
from runner_methods import (
    parse_file,
    sort_processes
)
'''
METHODS TO HELP RUN PROGRAM - NEEDED HERE TO USE THE LIST OF STATUSES
'''
def receive_signal(signal, frame):
    '''Will write to runner-status if USR1 signal received'''
    path = os.path.join(os.path.expanduser('~'),".runner-status")
    for _ in range(5):
        write_file(path)

        if (check_file(path) != 0):
            break

        time.sleep(1) #if nothing has been written to it, wait and try again
    
def write_file(filename):
    '''creates and writes to a file'''
    global statuses

    with open(filename, "w+") as f:
        if (len(statuses) > 0):
            f.write("\n".join(statuses))

def send_PID(pid):
    '''Creates or writes to exisitng file sending PID of current process'''
    path = os.path.join(os.path.expanduser('~'),".runner-pid")
    with open(path, "w+") as f:
        f.write(str(pid))
    
    check_file(path) #check to see if it has been successfully created

def create_statusf(filename):
    '''Create status file if it does not exist'''
    path = os.path.join(os.path.expanduser('~'), filename)
    try:
        with open(path, "r") as f:
            pass #it has already been created, don't need to create it
    except FileNotFoundError:
        with open(path, "w+") as f:
            f.write("")
    
    check_file(path)

def check_file(filename):
    '''Error checking to see if the file exists or anything has been written to it'''
    try:
        with open(filename, "r") as f:
            contents = []

            while True:
                line = f.readline().strip()

                if (line == ""):
                    break
                
                contents.append(line)
            
            return (len(contents))

    except FileNotFoundError:
        sys.stderr.write("file {} does not exist. File unsuccessfully created in runner program. Please check for errors.\n".format(filename)) 
        sys.exit(1)

'''
THE PROGRAM
'''
#reading, creating and sorting the processes from .runner.config
config_path = os.path.join(os.path.expanduser('~'), ".runner.conf")
processes = parse_file(config_path)
sort_processes(processes) 

#checking the existence/creating .runner-status
create_statusf(".runner-status")
statuses = [process.will_run_str() for process in processes]

#sending PID to .runner-pid
pid = os.getpid()
send_PID(pid)

index = 0
while processes:
    signal.signal(signal.SIGUSR1, receive_signal) #catching USR1 signal

    process = processes.pop(0)

    while (datetime.datetime.now().replace(microsecond=0) != process.run_date): #ignoring mircoseconds
        time.sleep(1)

    pid = os.fork()
    try:
        if (pid > 0):
            #parent
            time_lim = 55
            for _ in range(time_lim): #wait 55 seconds for a child process to return
                child_pid, status = os.waitpid(-1, os.WNOHANG)  #if any child process does not return instantly, just return 0 --> done by os.WNOHANG

                if (child_pid != 0): #that means a child had returned to the parent process. Don't need to wait anymore.
                    break

                time.sleep(1)
            
            #checking status of process
            statuses.insert(index, process.ran_str(status))

        elif (pid == 0):
            #child
            os.execv(process.path, process.param)

        else:
            #error
            statuses.append(index, process.ran_str(1))

    except ChildProcessError:
        # There are no child processes (either not created yet or killed)
        pass

    if (process.freq == "every"):
        new_run_date = process.run_date + datetime.timedelta(days = 7) #don't need to set new_day like in sort_process() as this is for the same day, next week
        process.set_run_date(new_run_date) 
        processes.append(process)
    
    else:
        statuses.pop(index + 1)
    
    index += 1

time.sleep(2) #waiting for two seconds in case the user wishes to obtain check the last status ran (before the runner.py exits)
print("nothing left to run")