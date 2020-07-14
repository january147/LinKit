#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Fri Mar 20 09:46:07 2020
# Author: January

import sys

def main():
    if len(sys.argv) < 1:
        print("pleas specify a file")
        return
    filename = sys.argv[1]
    print("{", end = '')
    with open(filename, "rb") as file:
        data = file.read()
    i = 1
    for byte in data:
        print("0x%02x"%(byte), end=',')
        if (i % 20) == 0:
            print()
        i += 1
    print("}")

if __name__ == "__main__":
    main()
