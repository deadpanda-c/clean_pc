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


list_of_size = []
parser = argparse.ArgumentParser()
parser.add_argument("path", help="list all files on this path")
parser.add_argument("-a", "--all", help="search on the whole system about the 10s biggest file", action="store_true")
parser.add_argument("-s", "--size", help="display the size of the file beside the name", action="store_true")
parser.add_argument("-S", "--sort", help="display the files from the littlest size to the biggest size", action="store_true")
parser.add_argument("-b", "--big", help="display the biggest file", action="store_true")
parser.add_argument("-l", "--little", help="display the littlest file", action="store_true")

args = parser.parse_args()

if args.path:
    if not os.path.isdir(args.path):
        print("\033[0;31m[*] ERROR: \033[0;37mThe path is invalid", file=sys.stderr)
        exit(127)
    for filename in os.listdir(args.path):
        file = os.path.join(args.path, filename)
        if os.path.isfile:
                if args.size:
                    size = os.path.getsize(file)
                    print(file, size)
"""
if (len(sys.argv) == 2):
    for filename in os.listdir(sys.argv[1]):                            # LIST ALL FILES IN THE PATH GIVEN AS ARGUMENTS
        file = os.path.join(sys.argv[1], filename)
        size = os.path.getsize(file)
        if os.path.isfile:
            print("{} {}".format(file, size))
            list_of_size.append(size)
    print("Original: {}".format(list_of_size))
    list_of_size.sort()
    print("Sorted: {}".format(list_of_size))
"""
