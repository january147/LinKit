#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Mon Feb 25 11:46:43 2019
# Author: January

import os
import datetime
import sys

def generate_journal():
    date = datetime.date.today()
    if len(sys.argv) > 1:
        title = '-'+sys.argv[1]
    else:
        title = ''
    journal_name = date.strftime('%Y-%m-%d' + title + '.md')
    if os.path.isfile(journal_name):
        print('%s already exists'%(journal_name))
    else:
        journal_file = open(journal_name, 'w')
        journal_file.close()
        print('%s generated'%(journal_name))

if __name__ == '__main__':
    generate_journal()
    



