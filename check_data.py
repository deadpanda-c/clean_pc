#!/bin/python3

import os
import sys
import argparse
import sqlite3

# ------------------------
#       SET ARGS
# ------------------------




# -----------------------
#       GLOBAL VAR
# -----------------------

HOMEDIR = os.path.expanduser("~")
CONFIG_FOLDER = os.path.join(HOMEDIR, ".clean_config")

# ------------------------
#       FUNCTION ZONE
# ------------------------

# generic function who return the list of data


def display_data(filename_list, size_list):
    for row in range(len(filename_list)):
        print("{:>8}     {:>10}".format(filename_list[row], size_list[row]))

def get_file_size(table_len, conn, cur):
    list_of_size = []
    cpt = 1
    while cpt <= table_len:
        cur.execute("SELECT size FROM file_c where file_id = '{}'".format(cpt))
        cpt += 1
        list_of_size.append(cur.fetchall()[-1][0])
    return list_of_size

def extract_filename(path_list):
    final_list = []
    for row in path_list:
        final_list.append(row[0])
    return final_list

def exec_sqlite_cmd(cmd, conn, cur):
    cur.execute(cmd)
    return cur.fetchall()

def open_db_file(file):
    
    conn = sqlite3.connect(os.path.join(CONFIG_FOLDER, file))    
    cur = conn.cursor()
    file_p_len = 0 
    path_list = []
    filename_list = []
    size_list = []
    # get the size of the file_p table
    try:
        file_p_len = len(exec_sqlite_cmd("SELECT * from file_p", conn, cur))
        path_list = exec_sqlite_cmd("SELECT absolute_path from file_p", conn, cur)
        filename_list = extract_filename(path_list)
        size_list = get_file_size(file_p_len, conn, cur)
        display_data(filename_list, size_list)
    except sqlite3.OperationalError:
        print("\033[31m[*] Error, the .db file is invalid ", file=sys.stderr)
        exit(-1)

def locate_n_open_db_file():
    if os.path.isdir(CONFIG_FOLDER):
        elem_config_folder = os.listdir(CONFIG_FOLDER)  # check if the db file exists
        for elem in elem_config_folder:
            elem = elem.split(".")
            try:
                if elem[1] == "db":
                    open_db_file(".".join(elem))
                    return
            except IndexError as err:
                continue

def check_db_exists():
    return_value = 84
    list_file = os.listdir(os.path.join(HOMEDIR, CONFIG_FOLDER))
    if len(list_file) == 0:
        return return_value    
    for file in list_file:
        if file.split(".")[-1] == "db":
           return_value = 0 
    return return_value

# ------------------------
#       MAIN ZONE
# ------------------------
if check_db_exists() == 84:
    print("\033[31m[*] No .db file found ! EXIT", file=sys.stderr)
    exit(-1)
# locate the db file
db_file = locate_n_open_db_file()
