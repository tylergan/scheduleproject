'''
AUTHOR: Tyler Gan
Date: 20/10/2020

This program contains all the necessary files to run RUNNER.PY. The following components contained in this program include:
    1. Process - Class (stores all process information as Process objects)
    2. parse_file() - function that will parse the configuration file and create Process objects; this works in conjunction with the subsequent functions listed:
        a. check_config() - This function checks the contents of the file and determines if there is anything present in the file. It also checks if the config file exists.
        b. valid_file() - this checks the validity of a line found in the config file. 
        c. valid_time() - This function determines if the time provided is in standard military format.
        d. sort_processes() - This function sorts the Process objects based on its run datetime attributes.
        e. time_diff - does the necessary calculations to determine, based on today's time, when the processes should next run, which is sent to parse_file() for it to assign
           each object a new datetime object.
'''

import datetime, sys, re, os

days_to_int = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class Process:
    def __init__(self, freq, day, time, path, param):
        self.freq = freq
        self.day = day
        self.time = time
        self.path = path
        self.param = param

        self.run_date = None
        self.ctime = None

    def set_run_date(self, date):
        self.run_date = date
        self.ctime = self.run_date.ctime()
    
    def set_new_day(self, day):
        self.day = day

    def will_run_str(self):
        return "will run at {} {}".format(self.ctime, " ".join(self.param))
    
    def ran_str(self, status):
        if (status == 0):
            return "ran {} {}".format(self.ctime, " ".join(self.param))
        else:
            return "error {} {}".format(self.ctime, " ".join(self.param))

def parse_file(path):
    '''parses configuration file to create process objects'''
    global days_to_int
    check_config(path)

    with open(path , "r") as f:
        processes = []

        while (True):
            line = f.readline().strip()
            check_dup_line = line
                
            line = line.split()
            if (line == []):
                break
            
            #error checking
            if (not valid_file(line)):
                sys.stderr.write("error in configuration: {}\n".format(" ".join(line)))
                sys.exit(1)

            #setting values for each field of a Process object
            if (line[0] == "every"):
                freq = "every"
            elif (line[0] == "on"):
                freq = "on"
            else:
                freq = "at"

            timespec = [elem for elem in line if ((line.index(elem) < line.index("run") and (elem != "every" and elem != "on" and elem != "at")))]
            path = line[line.index("run") + 1]
            param = [elem for elem in line if (line.index(elem) >= line.index("run") + 1)] #inclusive of the path

            #creating new processes
            for days in timespec[0].split(","):
                if (freq != "at"):
                    for hours in timespec[1].split(","):
                        if (freq == "every"):
                            processes.append(Process(freq, days, hours, path, param))
                        else:
                            processes.append(Process("once", days, hours, path, param))
                else:
                    #as we are running it today, days (in the list) will be equal to time (due to the format of the file)
                    processes.append(Process("once", days_to_int[datetime.date.today().weekday()], days, path, param))
            
            #assign datetime objects on when each object needs to run
            now = datetime.datetime.now()
            for process in processes:
                diff = time_diff(process, now)
                new_time = now + datetime.timedelta(days = diff)

                #setting the process's run_date field to a datetime object
                process.set_run_date(datetime.datetime(new_time.year, new_time.month, new_time.day, int(process.time[0:2]), int(process.time[2:4])))
                process.set_new_day(days_to_int[new_time.weekday()]) #done in the case of setting the process to run the next day (see time_diff() method)

            #check for duplicate run times
            check_duplicates = [str(process.run_date) for process in processes]
            if (len(check_duplicates) != len(set(check_duplicates))): 
                sys.stderr.write("error in configuration: {}\n".format(check_dup_line))
                sys.exit(1)
        
    return processes

def check_config(filename):
    '''Check if there is anything present in the file.'''
    try:
        with open(filename , "r") as f:
            contents = []

            while True:
                line = f.readline().strip()

                if (line == ""):
                    break
                
                contents.append(line)
            
            if (len(contents) == 0):
                sys.stderr.write("configuration file empty\n")
                sys.exit(1)

    except FileNotFoundError:
        sys.stderr.write("configuration file not found\n")
        sys.exit(1)

def valid_file(line):
    '''Checking validity of configuration file'''
    global days_to_int

    valid = True
    format_check = " ".join(line)

    match_format = re.search("^(on|every).*at.*run|^at.*run", format_check) #using Regex to find specifc format of "[(on|every)...]at...run"
    if (match_format):
        if re.search("^(on|every)", format_check): #for processes specfied with (on|every)

            #check if days are valid
            check_days = line[1].split(",")
            check_days = [day if (day in days_to_int) else (None) for day in check_days] 

            if (None in check_days):
                valid = False
            elif (len(check_days) != len(set(check_days))): #checking for duplicate days
                valid = False
            else:
                check_time = line[3].split(",") 

                #check if the parameters are valid and in army time format
                if (not valid_time(check_time)): 
                    valid = False
                elif(len(check_time) != len(set(check_time))): #duplicate times
                    valid = False
                else:
                    check_path = [elem for elem in line if line.index(elem) > line.index("run")] #check that the path is present
                    if (len(check_path) == 0):
                        valid = False

        else: #for formats starting with "at"
            check_time = line[1].split(",")
            if (not valid_time(check_time)):
                    valid = False
            elif(len(check_time) != len(set(check_time))):
                    valid = False
            else:
                check_path = [elem for elem in line if line.index(elem) > line.index("run")]
                if (len(check_path) == 0):
                    valid = False

    else:
        valid = False
    
    return valid

def valid_time(times):
    '''check if the parameters are valid and in army time format'''
    for time in times:
        if (len(time) != 4):
            return False
                    
        else:
            try:
                hour, minute = int(time[0:2]), int(time[2:4])
                if (not 0 <= hour < 24) or (not 0 <= minute < 59):
                    return False
            except ValueError:
                return False
    
    return True

def sort_processes(processes):
    '''Sort the list of Process objects by the date they are meant to be run'''
    processes.sort(key = lambda x: x.run_date) #sort the list of processes based on its run_date field (initialised to a datetime object)

def time_diff(process, now):
    '''Finds the difference between the current date and when the process is meant to be run, giving us a date and time when the process should run'''
    global days_to_int
 
    current_day = now.date().weekday()
    current_time = int("{}{}".format(now.hour, now.minute))

    #checking the day difference between today's day and the process run day
    days_diff = 0
    i = current_day
    while i != days_to_int.index(process.day):
        i += 1
        if (i > 6):
            i = 0
        days_diff += 1        

    #setting process to run next day if we have a process that will run on the same day but at an earlier than what is now
    if (days_diff == 0):
        if (current_time > int(process.time)): 
            days_diff = 1 #then set the time for the next day

    return days_diff