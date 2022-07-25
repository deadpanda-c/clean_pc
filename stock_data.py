#!/bin/python3

import os
import sys
import time
import argparse

NB_OF_FILES = 0
PATH = "."
DICT_OF_FILES = {}

    
def sort_the_files():
    sorted_dict = {}
    for filename in sorted(DICT_OF_FILES, key=DICT_OF_FILES.get, reverse=True):
        sorted_dict[filename] = os.path.getsize(filename)
    return sorted_dict

def invalid_path(path):
    if not os.path.exists(path):
        print("[\033[31m\u2718\033[37m] Invalid path !", file=sys.stderr)
        exit(-1)

def display_dict_content(dictionnary):
    for key, value in dictionnary.items():
        print("{} : {}".format(key, value))

def list_files_from_path():
    for i in files:
        files_path = os.path.join(root, i)
        sys.stdout.write("\033[K")
        if os.path.islink(files_path):
            continue    
        DICT_OF_FILES[files_path] = os.path.getsize(files_path)
        if len(root) > 32:
            sys.stdout.write("\rListing from {}... ({}/.../{})".format(PATH, (root[:len(root) // 2]), i))
        else:
            sys.stdout.write("\rListing from {}... ({})".format(PATH, files_path))
        sys.stdout.flush()        


def print_biggest_file(dict_file):
    cpt = 0
    if len(dict_file) > 10:
        for key in dict_file:
            if cpt == 10:
                break
            print(key)
            cpt += 1
    else:
        for key in dict_file:
            print(key)

invalid_path(PATH)

for root, cur_dir, files in os.walk(PATH):
    NB_OF_FILES += len(files)
    try:
        list_files_from_path()
    except Exception as err:
        print("\nThe error is: {}".format(err))
print("\n")
print("[\033[32m\u2714\033[37m] Listing completed !")

#display_dict_content(DICT_OF_FILES)

sorted_dict = sort_the_files()
print_biggest_file(sorted_dict)
