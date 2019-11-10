#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from LinKit_lib import options as op

USAGE = '[Usage] : abspath <relative_path>'

def main():
    raw_args, options = op.get_options_v2(sys.argv, ['h'])
    if "h" in options.keys():
        print(USAGE)
        return
    
    if len(raw_args) == 0:
        print(os.path.abspath("."))
    else:
        for item in raw_args:
            if not os.path.exists(item):
                print('no such file or directory')
                continue
            try:
                print(os.path.abspath(item))
            except:
                print('Unknown error')

if __name__ == '__main__':
    main()
