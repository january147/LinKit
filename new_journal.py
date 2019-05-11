#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Mon Feb 25 11:46:43 2019
# Author: January

import os
import datetime

def generate_journal():
    date = datetime.date.today()
    journal_name = date.strftime('%y-%m-%d.md')
    if os.path.isfile(journal_name):
        print('%s already exists'%(journal_name))
    else:
        journal_file = open(journal_name, 'w')
        journal_file.close()
        print('%s generated'%(journal_name))

if __name__ == '__main__':
    generate_journal()
    



