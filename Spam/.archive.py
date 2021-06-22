# import os, sys, datetime, time, signal
# from runner_methods import (
#     parse_file,
#     sort_processes
# )

# def send_PID(pid):
#     with open(".runner.pid", "w+") as file:
#         file.write(str(pid))

# def receive_signal(signal, frame):
#     '''Will write to runner.status if USR1 signal received'''
#     global statuses

#     with open(".runner.status", "w+") as file:
#         string = "\n".join(statuses)
#         file.write(string)
#     sys.exit()

# def timeout_signal(singal, frame):
#     '''Will raise Timeout Error if specifc area in code runs for time period longer than time set by signal.alarm'''
#     print("status timeout")
#     raise TimeoutError

# processes = parse_file(".runner.conf")

# pid = os.getpid()
# send_PID(pid)

# statuses = []

# sort_processes(processes)
# while processes:
#     signal.signal(signal.SIGUSR1, receive_signal) #catching USR1 signal
#     signal.signal(signal.SIGALRM, timeout_signal) #will timeout if PID not returned in 5 seconds

#     process = processes.pop(0)
#     record = "will run at, {} {}, {}".format(process.day, process.time, ", ".join(process.param))
#     statuses.append(record)

#     while (datetime.datetime.now().replace(second = 0, microsecond=0) != process.run_date): #ignoring seconds and mircoseconds
#         time.sleep(1)
    
#     success_msg = "ran, {} {}, {}".format(process.day, process.time, ", ".join(process.param))
#     error_msg = "error, {} {}, {}".format(process.day, process.time, ", ".join(process.param))

#     signal.alarm(5) #limiting process to 5 seconds before timing out as other processess have to run
#     try:    
#         pid = os.fork()
#         if (pid > 0):
#             #parent
#             wVal = os.wait()
#             statuses.append(success_msg)
#         elif (pid == 0):
#             #child
#             os.execv(process.path, process.param)
#         else:
#             #error
#             statuses.append(error_msg)

#     except Exception as e: #caused by Timeout Error due to timeout_singal method
#         statuses.append(error_msg)
    
#     finally:
#         signal.alarm(0) #reset alarm to have no timeout once process executes/timesout