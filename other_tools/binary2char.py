#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Fri Mar 20 09:46:07 2020
# Author: January

import sys
import math

USAGE = "[USAGE] binary2char <file>"

def main():
    if len(sys.argv) < 2:
        print(USAGE)
        return
    
    indentation = "    "
    print("{")

    filename = sys.argv[1]
    with open(filename, "rb") as file:
        data = file.read()
    
    line_len = 20
    total_len = len(data)
    rows = math.ceil(total_len / line_len)

    for row in range(rows):
        cols = min(line_len, total_len - row * line_len)
        if cols > 0:
            print(indentation, end="")
        else:
            break
        comma = ","
        for col in range(cols):
            i = row * line_len + col
            byte = data[i]
            if i == total_len - 1:
                comma = ""
            print("0x%02x"%(byte), end=comma)
        print()
    print("}")

if __name__ == "__main__":
    main()
