#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Sat Nov 30 23:28:50 2019
# Author: January

import sys
import pdb
from LinKit_lib import options

usage = '''value [-h] [-b|-d|-x] [<hex>|<decimal>]
-h show help info
-b set output form to binary
-d set output form to decimal
-x set output form to hex'''

f_hex = 16
f_decimal = 10
f_binary = 2
f_none = 0

def main():
    raw_args, input_options = options.get_options_v2(sys.argv, ['b', 'd', 'x', 'h'])
    auto_form = False
    if 'h' in input_options.keys():
        print(usage)
        exit(0)
    if "b" in input_options.keys():
        output_form = f_binary
    elif "d" in input_options.keys():
        output_form = f_decimal
    elif "x" in input_options.keys():
        output_form = f_decimal
    else:
        output_form = f_none
        auto_form = True

    if len(raw_args) > 0:
        count = 1
        for num in raw_args:
            if num.startswith("0x") or num.startswith("0X"):
                input_form = f_hex
                if auto_form is True:
                    output_form = f_decimal
            else:
                input_form = f_decimal
                if auto_form is True:
                    output_form = f_hex

            try:
                num = int(num, input_form)
            except:
                print("%s is not a valid num"%(num))
                continue

            if output_form == f_decimal:
                print("%d "%(num), end=" ")
            elif output_form == f_hex:
                print(hex(num), end=" ")
            elif output_form == f_binary:
                print(bin(num), end=" ")
            else:
                print("unknow output type:%s"% output_form)
            # ten numbers every line
            if count % 10 == 0:
                print()
            count += 1
    # if output doesn't end up with a line break, add one
    if (count - 1) % 10 != 0:
        print()
        
            
if __name__ == "__main__":
    main()
