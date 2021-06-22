'''
AUTHOR: Tyler Gan
Date: 20/10/2020

This program runs RUNSTATUS.PY. The purpose of this program is to obtain the current status of the RUNNER.PY and output it to STDOUT.

The program contains the following functions:
    1. read_file() - This function reads both .runner-pid which is used to send a USR1 signal to RUNNER.PY and is used to read the contents of .runner-status. If the file does
                     does not exist, the program writes to STDERR.
'''

import os, time, sys

def read_file(filename):
    '''Reads .runner-pid and .runner-status and also checks for their existence.'''
    contents = []
    path = os.path.join(os.path.expanduser('~'), filename)
    try:
        with open(path, 'r') as f:
            while True:
                line = f.readline().strip()
                if (line == ""):
                    break
                contents.append(line)
        
        return contents

    except FileNotFoundError:
        sys.stderr.write("file {} does not exist. File unsuccessfully created in runner program. Please check for errors.\n".format(filename))
        sys.exit(1)

testing = False
if (len(sys.argv[1:]) > 0):
    testing = True

pidfile = ".runner-pid"
statusfilename = ".runner-status"

#read from .runner-pid
pid = read_file(pidfile)[0]

#sending USR1 signal
usr1_sig = ["/bin/kill", "-s", "USR1", pid]
pid = os.fork()
if (pid > 0):
    #parent
    for _ in range(3):
        child_pid, status = os.waitpid(-1, os.WNOHANG)

        if (child_pid != 0):
            break
        
        time.sleep(1)
    
    if (status != 0):
        sys.exit(1)
        
elif (pid == 0):
    #child
    os.execv(usr1_sig[0], usr1_sig)
    
else:
    #error
    sys.stderr.write("Error encountered in forking process.\n")
    sys.exit(1)

#read from the .runner-status
for _ in range(5):
    txt = read_file(statusfilename)
    if (len(txt) != 0):
        print("\n".join(txt))
        break
    
    if (not testing):
        time.sleep(1)

else:
    sys.stderr.write("status timeout\n")

path = os.path.join(os.path.expanduser('~'), statusfilename)

#reset the status file to nothing
try:
    with open(path, "w") as f:
        f.truncate(0)
except FileNotFoundError:
        sys.stderr.write("file {} does not exist. File unsuccessfully created in runner program. Please check for errors.\n".format(statusfilename))
        sys.exit(1)
