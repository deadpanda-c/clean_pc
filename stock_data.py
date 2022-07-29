#!/bin/python3

import sqlite3
import os
import sys
import datetime
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

def move_the_db_file(db_file):
    homedir = os.path.expanduser("~")
    if not os.path.isdir("{}/.clean_config".format(homedir)):
        os.system("mkdir {}/.clean_config".format(homedir))
    os.system("cp {} {}/.clean_config".format(db_file, homedir))
def get_file_ext(filename):
    path_exploded = filename.split("/")
    file = path_exploded[-1]
    file_exploded = file.split(".")
    if len(file_exploded) > 1:
        return file_exploded[-1]
    return "none"

def insert_into_table(conn, cur, sorted_dict):
    if args.size_from:
        min_size = int(args.size_from)
    else:
        min_size = pow(10, 8) # 100 MB
        pass
        # 10 MB

    for filename, size in sorted_dict.items():
        extension = get_file_ext(filename)
        abs_path = os.path.abspath(filename)
        if not os.path.exists(filename) or os.path.islink(filename):
            continue
        if size >= min_size:
            cur.execute("""
                INSERT OR IGNORE INTO file_p (absolute_path, extension) VALUES ('{}', '{}')
                    """.format(abs_path, extension))
            cur.execute("""
                INSERT INTO file_c (file_id, check_date, size) VALUES 
                (
                    (SELECT file_id from file_p where absolute_path = '{}'),
                    DATETIME('now', '+2 hours', 'localtime'),
                    '{}'
                )
                    """.format(abs_path, size))
def create_table(conn, cur):
    # first table
    cur.execute("""
            CREATE TABLE IF NOT EXISTS file_p (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                absolute_path varchar(255) NOT NULL UNIQUE,
                extension varchar(255) NOT NULL
            )
    """)
    # second table
    cur.execute("""
            CREATE TABLE IF NOT EXISTS file_c (
                file_id int NOT NULL,
                check_date DATETIME DEFAULT SESSIONTIMESTAMP, 
                size int NOT NULL,
                FOREIGN KEY (file_id) REFERENCES file_p (file_id)
            )
    """)

def check_if_in(conn, cur, sorted_dict):
    cur.execute("SELECT * FROM file_p WHERE file_id = 1")
    result = cur.fetchall()

def connect_to_db(sorted_dict):
    if args.db_name:
        db_file = args.db_name
    else:
        db_file = "clean.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    create_table(conn, cur)
    insert_into_table(conn, cur, sorted_dict)
    check_if_in(conn, cur, sorted_dict)
    conn.commit()
    conn.close()
    return db_file

def sort_the_files():
    sorted_dict = {}
    for filename in sorted(DICT_OF_FILES, key=DICT_OF_FILES.get, reverse=True):
        if os.path.islink(filename) or not os.path.exists(filename):
            continue
        sorted_dict[filename] = os.path.getsize(filename)
    return sorted_dict

def check_invalid_path(path):
    if not os.path.exists(path):
        exit(-1)


def list_files_from_path():
    for i in files:
        files_path = os.path.join(root, i)
        if os.path.islink(files_path) or not os.path.exists(files_path):
            continue    
        DICT_OF_FILES[files_path] = os.path.getsize(files_path)

# -----------------------------
#           START
# -----------------------------

check_invalid_path(PATH)

for root, cur_dir, files in os.walk(PATH):
    NB_OF_FILES += len(files)
    list_files_from_path()


sorted_dict = sort_the_files()
db_file = connect_to_db(sorted_dict)
move_the_db_file(db_file)
