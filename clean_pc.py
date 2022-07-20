#!/bin/python3

"""Arguments: 
    -h: display help menu
    -s: display size of the file with the name
    -S: display the files in from the littlest to the biggest
    -b: display the biggest file
    -l: display the littlest file

"""
import math
import datetime
import argparse
import os
import sys

# FUNCTIONS ZONE

## Generic functions
def display_date(file):
    getmtime_numeric = os.path.getmtime(file)
    last_modif = datetime.datetime.fromtimestamp(getmtime_numeric).replace(microsecond=0)
    print("[{}] ->".format(last_modif), end=" ")


def display_sorted(dict_file):
    for value in sorted(dict_file, key=dict_file.get):
        if args.size:
            display_size(value)
        else:
            print(value, end="")

def display_size(file):
    unit = None
    units = ["bytes", "KB", "MB", "GB"]
    size = os.path.getsize(file)
    if size < 1000:
        unit = units[0]    
    if size >= 1000 and size < pow(10, 6):
        unit = units[1]
        size /= 1000
    if size >= pow(10, 6) and size < pow(10, 9):
        unit = units[2]
        size /= pow(10, 6)
    if (size >= pow(10, 9)):
        size /= pow(10, 9)
        unit = units[3]
    print("{} -> {} {}".format(file, round(size, 1), unit))

def pick_the_smallest(dict_file):
    return min(dict_file, key=dict_file.get)

def pick_the_biggest(dict_file):
    return max(dict_file, key=dict_file.get)

## Other functions

def display_the_biggest_or_littlest(dict_file):
    if args.little:
        if args.size:
            display_size(pick_the_smallest(dict_file))
        else:
            print(pick_the_smallest(dict_file))
    if args.big:
        if args.size:
            display_size(pick_the_biggest(dict_file))
        else:
            print(pick_the_biggest(dict_file))

# SETTING UP ARGUMENT PARSER
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", help="list all files in the given path")
parser.add_argument("-s", "--size", help="display the size of the file beside the name", action="store_true")
parser.add_argument("-S", "--sort", help="display the files from the littlest size to the biggest size", action="store_true")
parser.add_argument("-d", "--date", help="display the last time the file was modificated", action="store_true")
parser.add_argument("-b", "--big", help="display the biggest file", action="store_true")
parser.add_argument("-l", "--little", help="display the littlest file", action="store_true")

args = parser.parse_args()

# OTHER VARIABLES

is_flag = False
is_sort_flag = False
is_big_little_flag = False

if args.path:
    path = args.path
else:
    path = "/var/log"

if os.path.isdir(path):
    file_dict = {}
    for filename in os.listdir(path):
        filename = os.path.join(path, filename)
        if (filename != '.' and filename != '..'):
            file_dict[filename] = os.path.getsize(filename)
    for filename in file_dict:
        if args.big or args.little:
            is_flag = True
            is_big_little_flag = True
            break
        if args.sort: # Condition for sort flag        
            is_flag = True
            is_sort_flag = True
            break
        if args.size:  # Condition for size flag
            display_size(filename)
            is_flag = True
        if args.date:
            display_date(filename)
        if not is_flag:
            print(filename)
    if is_sort_flag:
        display_sorted(file_dict)
    if is_big_little_flag:
        display_the_biggest_or_littlest(file_dict)
else: # if the path is not valid, exit with error message
    print("\033[;31mError: \033[;37mPath is invalid", file=sys.stderr)
    exit(-1)
