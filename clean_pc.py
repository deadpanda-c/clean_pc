#!/bin/python3

import os
import sys


if (len(sys.argv) == 2):
    if not os.path.isdir(sys.argv[1]):
        print("\033[0;31m[*] ERROR: \033[0;37mThe path is invalid", file=sys.stderr)
        exit(127)
    for filename in os.listdir(sys.argv[1]):                            # LIST ALL FILES IN THE PATH GIVEN AS ARGUMENTS
        file = os.path.join(sys.argv[1], filename)
        if os.path.isfile:
            print(file)
