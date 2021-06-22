import sys

try:
    with open("file_does_not_exist", "r"):
        pass
except FileNotFoundError:
    print("The file was not found, but I will not exit this program with a status greater than 0")
