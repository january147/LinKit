#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Mon Feb 18 22:01:46 2019
# Author: January

import os
import sys
import datetime
from LinKit_lib import options as op

USAGE = '[Usage] stamp <filename> [type]'
FILE_INFO = {
    'py' : '#!/usr/bin/python3\n'
           '# -*- coding: utf-8 -*-\n',
    'sh' : '#!/bin/bash\n',
    
}
COMMENT_FLAG = {
    'py' : '#',
    'sh' : '#',
    'c'  : '//',
    'h'  : '//',
    'cpp': '//',
    'java' : '//'
}

EXECUTE_TYPE = ['py', 'sh']

FILE_FORMAT = {
    'py' : 'def main():\n'
           '    pass\n'
           'if __name__ == "__main__":\n'
           '    main()\n',

    'c'  : '#include<stdio.h>\n'
           'int main() {\n'
           '    return 0;\n'
           '}\n'
}

class Config(object):
    TYPE = 'py'
    AUTHOR = 'January'
    COMMENT_FLAG = '#'


def generateStamp():
    part_header = ''
    date = Config.COMMENT_FLAG + ' Date: ' + datetime.datetime.now().ctime() + '\n'
    author = Config.COMMENT_FLAG + ' Author: ' + Config.AUTHOR + '\n'
    if Config.TYPE in FILE_INFO.keys():
        part_header = FILE_INFO[Config.TYPE]
    
    header = part_header + date + author
    return header

# 生成文件初始模板内容
def generateNewFormat():
    return FILE_FORMAT[Config.TYPE]

def stamp(filename):
    # 从扩展名读取文件类型
    file_ext = filename.split('.')[-1]
    Config.TYPE = file_ext
    if Config.TYPE in COMMENT_FLAG.keys():
        Config.COMMENT_FLAG = COMMENT_FLAG[Config.TYPE]
    # 生成新文件名为xxx.stamping
    working_filename = filename + ".stamping"
    # 创建新文件
    new_file = open(working_filename, 'w')
    new_file.write(generateStamp())
    # 复制源文件数据到新文件
    try:
        with open(filename, 'r') as old_file:
            while True:
                content = old_file.read(4096)
                if content != '':
                    new_file.write(content)
                else:
                    break
        # 删除原文件
        os.remove(filename)
    # 原文件不存在则跳过该步骤
    except:
        # 给创建的新文件写入一些模板化内容
        if Config.TYPE in FILE_FORMAT.keys():
            new_file.write(generateNewFormat())
            
            
    new_file.close()
    os.rename(working_filename, filename)
    # 对脚本文件加入可执行权限(只在linux上使用)
    if sys.platform == "linux" and Config.TYPE in EXECUTE_TYPE:
        os.system('chmod 755 ' + filename)
    
def main():
    raw_args, options = op.get_options_v2(sys.argv, ['h'])
    if 'h' in options.keys() or len(raw_args) == 0:
        print(USAGE)
        return
    
    for item in raw_args:
        stamp(item)

if __name__ == '__main__':
    main()
    



