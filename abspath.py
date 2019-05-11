#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

def main():
    try:
        filename = sys.argv[1]
    except:
        print('[Usage] : abspath <relative_path>')
        return
    
    if not os.path.exists(filename):
        print('no such file or directory')
        return
    
    try:
        print(os.path.abspath(filename))
    except:
        print('Unknown error')
        return

if __name__ == '__main__':
    main()