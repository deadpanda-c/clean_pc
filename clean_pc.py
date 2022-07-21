#!/bin/python3

"""Arguments: 
    -h: display help menu
    -s: display size of the file with the name
    -S: display the files in from the littlest to the biggest
    -b: display the biggest file
    -l: display the littlest file

"""
import sqlite3
import math
import datetime
import argparse
import os
import sys

# FUNCTIONS ZONE

## Generic functions
def create_db(conn, cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS files
                (filename, first_checkpoint, second_checkpoint, third_checkpoint)''')
    print("[*] Table was created ! Check with: sqlite3 {}.db".format(args.save))
    return conn, cur

def print_the_db(conn, cur):
    row = ()
    with conn:
        cur.execute("SELECT * FROM files")
    row = cur.fetchone()

def get_db_data(conn, cur, col):
    with conn:
        cur.execute("SELECT {} FROM files".format(col))
    return cur.fetchone()[0] 

def edit_checkpoint_size(conn, cur, data):
    # check si le second checkpoint est vide ou pas
    second_checkpoint = get_db_data(conn, cur, "second_checkpoint")
    third_checkpoint = get_db_data(conn, cur, "third_checkpoint")
    if not second_checkpoint:
        for filename in data:
            cur.execute("UPDATE files set second_checkpoint = '{}' where filename = '{}'".format(os.path.getsize(filename), filename))
            print("[*] Database updated !")
        return 0
    if not third_checkpoint:
        for filename in data:
            cur.execute("UPDATE files set third_checkpoint = '{}' where filename = '{}'".format(os.path.getsize(filename), filename))
            print("[*] Database updated bis!")
        return 0
    # check si le troisieme checkpoint vide ou pas
    return 1

def save_in_db(file_dict):
    if os.path.exists("{}.db".format(args.save)):
        conn = sqlite3.connect("{}.db".format(args.save))
        cur = conn.cursor()
        edit_checkpoint_size(conn, cur, file_dict)
        # go to the second and third checkpoint
    else:
        conn = sqlite3.connect("{}.db".format(args.save))
        cur = conn.cursor()
        conn, cur = create_db(conn, cur) # Creation of the database
        for data in file_dict:
            cur.execute("INSERT INTO files (filename, first_checkpoint) VALUES ('{}', '{}')".format(data, file_dict[data]))
        print("[*] Datas are saved in the database at : {}.db".format(args.save))
        # create the database, and fill the first checkpoint
    conn.commit()
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
parser.add_argument("--save", help="save file's data in a sqlite database (the given file)")

args = parser.parse_args()

# OTHER VARIABLES

is_flag = False
is_sort_flag = False
is_big_little_flag = False
is_db = False

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
    if args.save:
        is_db = True
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
        if not is_flag and not is_db:
            print(filename)
    
    if is_db:
        save_in_db(file_dict)
    if is_sort_flag:
        display_sorted(file_dict)
    if is_big_little_flag:
        display_the_biggest_or_littlest(file_dict)
else: # if the path is not valid, exit with error message
    print("\033[;31mError: \033[;37mPath is invalid", file=sys.stderr)
    exit(-1)
