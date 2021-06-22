'''
AUTHOR: Tyler Gan
Date: 20/10/2020

READ:
This is the TEST version of the runner.py program; THIS IS NOT THE MAIN RUNNER PROGRAM. The following modifications have been made for TESTING PURPOSES:
    1) Takes in different config files using sys.argv
    2) The time to wait (where you would sleep until you hit the reach the program run time) has been modified to 0.5 seconds per program.
    3) The format of the output obtained by runstatus.py will convert all date-related information to "XX" as the output of these dates may vary depending on when the test
       case is being run.
    
The original code which has been either modified or deleted has been left in comment blocks to show how the original program was meant to function.

Everything else has been left untouched.
'''

import os, sys, datetime, time, signal
from run_test_methods import (
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
    test_statuses = []

    #please note that the code BELOW is used for TESTING purposes only. We are replacing the date with XX as testing could be done at any time.
    for status in statuses:
        status = status.split()
        i = 0
        while (i < len(status)):
            if (status[i] == "ran") or (status[i] == "run") or (status[i] == "error"):

                diff = 0
                if (status[i] == "ran") or (status[i] == "error"):
                    diff = 1
                else:
                    diff = 2

                for j in range(i + diff, i + diff + 3):
                    status[j] = "XX"
                
                test_statuses.append(" ".join(status))
                break

            i += 1
    #The code ABOVE is for TESTING purposes only.

    with open(filename, "w+") as f:
        if (len(test_statuses) > 0):
            f.write("\n".join(test_statuses))

    '''
    ORIGINAL CODE:      

    global statuses

    with open(filename, "w+") as f:
        if (len(statuses) > 0):
            f.write("\n".join(statuses))

    '''

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
#reading, creating and sorting the processes from .runner.config -note that the below config_path is different to what it is in the original runner
config_path = os.path.join("tests", sys.argv[1], sys.argv[2], "{}.conf".format(sys.argv[2]))

'''
ORIGINAL CODE:
config_path = os.path.join(os.path.expanduser('~'), ".runner.conf")
'''
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

    #Note that the code below is the section that has been modified to reduce wait time between the current time and process run time.

    '''
    ORIGINAL CODE:
    
    while (datetime.datetime.now().replace(microsecond=0) != process.run_date): #ignoring mircoseconds
        time.sleep(1)
    '''

    before_time = process.run_date - datetime.timedelta(seconds=0.5)

    while (before_time.replace(microsecond=0) != process.run_date): #ignoring mircoseconds
        time.sleep(0.5)
        before_time += datetime.timedelta(seconds=0.5)

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

time.sleep(2)
print("nothing left to run")