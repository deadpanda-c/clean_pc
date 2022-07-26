#!/bin/python3

import sqlite3
import os
import sys
import time
import argparse

# --------------------------
#       PARSE ARGUMENT
# --------------------------
parser = argparse.ArgumentParser()

parser.add_argument("PATH", help="search the biggest files in this PATH")
parser.add_argument("--db-name", help="specify the name of the .db file (default name is clean.db)", action="store_true")
parser.add_argument("-s", "--size-from", help="precise the size minimum of a file for being in the database (so for 1 KB: {} --size_from 1000)".format(sys.argv[0]))
args = parser.parse_args()

# -------------------------
#       GLOBAL VAR
# -------------------------

PATH = args.PATH

NB_OF_FILES = 0

DICT_OF_FILES = {}

# --------------------------
#       FUNCTION ZONE
# --------------------------

def insert_into_table(conn, cur, sorted_dict):
    if args.size_from:
        min_size = int(args.size_from)
    else:
        min_size = pow(10, 8) # 100 MB
        pass
        # 10 MB

    for filename, size in sorted_dict.items():
        abs_path = os.path.abspath(filename)
        if not os.path.exists(filename) or os.path.islink(filename):
            continue
        if size >= min_size:
            cur.execute("""
                INSERT INTO file_p (absolute_path) VALUES ('{}')
                    """.format(abs_path))
def create_table(conn, cur):
    # first table
    cur.execute("""
            CREATE TABLE IF NOT EXISTS file_p (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                absolute_path varchar(255) NOT NULL
            )
    """)
    # second table
    cur.execute("""
            CREATE TABLE IF NOT EXISTS file_c (
                child_id int IDENTITY(1, 1) PRIMARY KEY,
                file_id int NOT NULL,
                check_date DATE NOT NULL,
                size int NOT NULL,
                FOREIGN KEY (file_id) REFERENCES file_p (file_id)
            )
    """)

def connect_to_db(sorted_dict):
    if args.db_name:
        db_file = args.db_name
    else:
        db_file = "clean.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    create_table(conn, cur)
    print("Table are created !")
    insert_into_table(conn, cur, sorted_dict)
    conn.commit()
    conn.close()

def sort_the_files():
    sorted_dict = {}
    for filename in sorted(DICT_OF_FILES, key=DICT_OF_FILES.get, reverse=True):
        if os.path.islink(filename) or not os.path.exists(filename):
            continue
        sorted_dict[filename] = os.path.getsize(filename)
    return sorted_dict

def check_invalid_path(path):
    if not os.path.exists(path):
        print("[\033[31m\u2718\033[37m] Invalid path !", file=sys.stderr)
        exit(-1)

def display_dict_content(dictionnary):
    for key, value in dictionnary.items():
        print("{} : {}".format(key, value))

def list_files_from_path():
    for i in files:
        files_path = os.path.join(root, i)
        if os.path.islink(files_path) or not os.path.exists(files_path):
            continue    
        DICT_OF_FILES[files_path] = os.path.getsize(files_path)

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

# -----------------------------
#           START
# -----------------------------

check_invalid_path(PATH)

print("Listing file...") # TO REMOVE !
for root, cur_dir, files in os.walk(PATH):
    NB_OF_FILES += len(files)
    list_files_from_path()

print("[\033[32m\u2714\033[37m] Listing completed !")

print("Sorting...")
sorted_dict = sort_the_files()
print("Displaying...")
print_biggest_file(sorted_dict)
print("Connection to the db...")
connect_to_db(sorted_dict)

