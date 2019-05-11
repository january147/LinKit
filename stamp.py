#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Mon Feb 18 22:01:46 2019
# Author: January

import os
import sys
import datetime

USAGE = '[Usage] stamp <filename> [type]'
STAMP = {
    'python3' : '#!/usr/bin/python3&'
                '# -*- coding: utf-8 -*-&',
    'sh'      : '#!/bin/bash&'
}

class Config(object):
    TYPE = 'python3'
    AUTHOR = 'January'
    LINE_BREAK = '\n'
    COMMENT_FLAG = '#'
    @staticmethod
    def config():
        for key in STAMP.keys():
            STAMP[key] = STAMP[key].replace('&', Config.LINE_BREAK)
        if len(sys.argv) >= 3:
            Config.TYPE = sys.argv[2]

def generateStamp():
    date = Config.COMMENT_FLAG + ' Date: ' + datetime.datetime.now().ctime() + Config.LINE_BREAK
    author = Config.COMMENT_FLAG + ' Author: ' + Config.AUTHOR + Config.LINE_BREAK
    stamp = STAMP[Config.TYPE] + date + author + Config.LINE_BREAK
    return stamp

def stamp():
    try:
        filename = sys.argv[1]
    except:
        print(USAGE)
        return
    
    working_filename = filename + ".stamping"
    new_file = open(working_filename, 'w')
    new_file.write(generateStamp())
    try:
        with open(filename, 'r') as old_file:
            while True:
                content = old_file.read(4096)
                if content != '':
                    new_file.write(content)
                else:
                    break
        os.remove(filename)
    except:
        pass
    new_file.close()
    os.rename(working_filename, filename)
    os.system('chmod 755 ' + filename)
    
    
if __name__ == '__main__':
    Config.config()
    stamp()
    



