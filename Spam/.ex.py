import signal, re, time, os, sys
# def handler(signum, frame):
#     print ('Here you go')

# while True:
#     signal.signal(signal.SIGINT, handler)
#     while True:
#         pass

# at 0900,1200 run /home/bob/myprog
#on Tuesday,Wednesday at 1300,1500 run /home/alex/myprog p1
# valid = re.search("^(on|at|every)?.*?at.*run", string)
# string = "at 0900,1200 run /home/bob/myprog"
# string = string.split(" ")
# string = " ".join([elem for elem in string if (string.index(elem) <= string.index("run"))])

# valid = re.search("^(on|every).*at.*run|^at.*run.*", "on Tuesday,Wednesday at 1300,1500 run /home/alex/myprog p1")
# print(valid)
# if valid:
#     print(True)
# else:
#     print(False)

# pid = os.fork()
# if (pid > 0):
#     #parent
#     i = 0
#     while i <= 5:
#         wVal = os.waitpid(-1, os.WNOHANG)
#         i += 1
#         time.sleep(1)
#     print(wVal)
        
# elif (pid == 0):
#     #child
#     print("hello")
#     time.sleep(30)
# else:
#     #error
#     raise OSError("Error encountered in forking process.")

# def write(filename):
#     with open(filename, "w+") as f:
#         f.write("Hello")

# def find_runstatus(filename):
#     try:
#         with open(filename, "w+") as f:
#             return True
#     except FileNotFoundError:
#         return False

# path = os.path.join(os.path.expanduser('~'),".runner.status")

# if not find_runstatus(path):
#     write(path)

sys.stderr.write("hello\n")
