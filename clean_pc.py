#!/bin/python3

"""Arguments: 
    -h: display help menu
    -s: display size of the file with the name
    -S: display the files in from the littlest to the biggest
    -b: display the biggest file
    -l: display the littlest file

"""

import argparse
import os
import sys

# FUNCTIONS ZONE

## Generic functions
def display_sorted(dict_file):
    for value in sorted(dict_file, key=dict_file.get):
        if args.size:
            display_size(value)
        else:
            print(value)

def display_size(file):
    size = os.path.getsize(file)
    print("{} -> {} bytes".format(file, size))

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
parser.add_argument("path", help="list all files on this path")
parser.add_argument("-a", "--all", help="search on the whole system about the 10s biggest file", action="store_true")
parser.add_argument("-s", "--size", help="display the size of the file beside the name", action="store_true")
parser.add_argument("-S", "--sort", help="display the files from the littlest size to the biggest size", action="store_true")
parser.add_argument("-d", "--date", help="display the last time the file was modificated")
parser.add_argument("-b", "--big", help="display the biggest file", action="store_true")
parser.add_argument("-l", "--little", help="display the littlest file", action="store_true")

args = parser.parse_args()

# OTHER VARIABLES

is_flag = False
is_sort_flag = False
is_big_little_flag = False

if os.path.isdir(args.path):
    file_dict = {}
    for filename in os.listdir(args.path):
        file_dict[filename] = os.path.getsize(filename)
    for filename in file_dict:
        if args.little:
            is_flag = True

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
        if not is_flag:
            print(filename)
    if is_sort_flag:
        display_sorted(file_dict)
    if is_big_little_flag:
        display_the_biggest_or_littlest(file_dict)
else: # if the path is not valid, exit with error message
    print("\033[;31mError: \033[;37mPath is invalid", file=sys.stderr)
    exit(-1)
