#!/bin/python3

"""Arguments: 
    -h: display help menu
    -s: display size of the file with the name
    -S: display the files in from the littlest to the biggest
    -b: display the biggest file
    -l: display the littlest file

"""
import sqlite3
import datetime
import argparse
import os
import sys
import pprint

# FUNCTIONS ZONE

## Generic functions

"""compare_checkpoint(conn, cur, data)
    
    It will compare each size given in the database 
    and will check if it's an increasing file or not
"""
def compare_checkpoint(conn, cur, data):
    first_checkpoint = 0
    second_checkpoint = 0
    third_checkpoint = 0
    cur.execute("SELECT * FROM files")
    table = cur.fetchall()
    with open("list_of_increasing_file.txt", "a") as file:
        file.write("HERE YOU CAN FIND THE LIST OF FILE THAT CONTINUE TO INCREASE\n")
        file.close()
    for rows in table:
        first_checkpoint = int(rows[1])
        second_checkpoint = int(rows[2])
        third_checkpoint = int(rows[3])
        if (third_checkpoint > second_checkpoint and third_checkpoint > first_checkpoint) \
                and (second_checkpoint > first_checkpoint):
                with open("list_of_increasing_file.txt", "a") as file:
                    file.write("- {}: {}".format(rows[0], third_checkpoint))
                    file.close()

""" create_db(conn, cur)

    Create a table and store it in a file given by the user in the arguments
"""

def create_db(conn, cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS files
                (filename, first_checkpoint, second_checkpoint, third_checkpoint)''')
    return conn, cur

""" print_the_db()

    print the content of the db
"""

def print_the_db():
    conn = sqlite3.connect("{}".format(args.display_db))
    cur = conn.cursor()
    table = ()
    with conn:
        cur.execute("SELECT * FROM files")
    table = cur.fetchall()
    for rows in table:
        for col in rows:
            print(col, end=" ")
        print('\n--------------------------------------------')


""" get_db_data(conn, cur, col)

    short function that will return the data from a specific cell choose
"""

def get_db_data(conn, cur, col):
    with conn:
        cur.execute("SELECT {} FROM files".format(col))
    return cur.fetchone()[0] 

""" edit_checkpoint_size(conn, cur, data)

    Edit the second and the third checkpoint if they are empty, one by one
"""

def edit_checkpoint_size(conn, cur, data):
    second_checkpoint = get_db_data(conn, cur, "second_checkpoint")
    third_checkpoint = get_db_data(conn, cur, "third_checkpoint")
    if not second_checkpoint:
        for filename in data:
            cur.execute("UPDATE files set second_checkpoint = '{}' where filename = '{}'".format(os.path.getsize(filename), filename))
        return 0
    if not third_checkpoint:
        for filename in data:
            cur.execute("UPDATE files set third_checkpoint = '{}' where filename = '{}'".format(os.path.getsize(filename), filename))
        return compare_checkpoint(conn, cur, data)
    return 1

""" save_in_db(file_dict)

    if there is the .db file, it will add the second checkpoint and the third checkpoint
    else it will create the db, and save the name and the actual size of the file in a .db file
"""

def save_in_db(file_dict):
    if os.path.exists("{}.db".format(args.save)):
        conn = sqlite3.connect("{}.db".format(args.save))
        cur = conn.cursor()
        edit_checkpoint_size(conn, cur, file_dict)
    else:
        conn = sqlite3.connect("{}.db".format(args.save))
        cur = conn.cursor()
        conn, cur = create_db(conn, cur) # Creation of the database
        for data in file_dict:
            cur.execute("INSERT INTO files (filename, first_checkpoint) VALUES ('{}', '{}')".format(data, file_dict[data]))
        print("[*] Datas are saved in the database at : {}.db".format(args.save))
    conn.commit()

"""display_date(file)
    
    display the last time the file was edited 
"""

def display_date(file):
    getmtime_numeric = os.path.getmtime(file)
    last_modif = datetime.datetime.fromtimestamp(getmtime_numeric).replace(microsecond=0)
    print("[{}] ->".format(last_modif), end=" ")

""" display_sorted(dict_file)

    list the file in an ascending order
"""

def display_sorted(dict_file):
    for value in sorted(dict_file, key=dict_file.get):
        if args.size:
            display_size(value)
        else:
            print(value, end="")

""" display_size(file)

    print the size of the file beside the name
"""

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

""" pick_the_smallest(dict_file)

    return the smallest file from the path given as arguments
"""

def pick_the_smallest(dict_file):
    return min(dict_file, key=dict_file.get)

"""pick_the_biggest(dict_file)

    return the biggest file from the path given as argument
"""

def pick_the_biggest(dict_file):
    return max(dict_file, key=dict_file.get)

## Other functions

"""display_the_biggest_or_littlest(dict_file)

    main function who check if it'll display the smallest and/or the biggest file
"""

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
parser.add_argument("--display-db", help="display the database's table if there's one")
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


## MAIN PROGRAM
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
    if args.display_db:
        print_the_db()
    if is_sort_flag:
        display_sorted(file_dict)
    if is_big_little_flag:
        display_the_biggest_or_littlest(file_dict)
else: # if the path is not valid, exit with error message
    print("\033[;31mError: \033[;37mPath is invalid", file=sys.stderr)
    exit(-1)
