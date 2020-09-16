#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Mon Feb 18 22:01:46 2019
# Author: January

import os
import sys
import datetime
from LinKit_lib import options as op
from LinKit_lib import jlib


class Config(object):
    TYPE = ''
    isMultilineComment = False
    COMMENT_FLAG = ''
    # user config
    AUTHOR = 'January'

USAGE = '''[Usage] stamp <filename>
try "stamp --list" to see supported file type'''

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
    'java' : '//',
    "md" : ''
}

MULTILINE_COMMENT_FLAG = {
    'c' : ('/*', '*/', '*'),
    'h'  : ('/*', '*/', '*'),
    'cpp' : ('/*', '*/', '*'),
    'java' : ('/*', '*/', '*'),
    'md' : ('<!--', "-->", "-")
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

    
log = jlib.logger()

def generateStamp():
    file_info = ''
    header_start = ''
    header_end = ''
    
    if Config.isMultilineComment:
        header_start = Config.COMMENT_FLAG[0] + Config.COMMENT_FLAG[2] + "\n"
        header_end = ' ' + Config.COMMENT_FLAG[1] + '\n'
        content_prefix = ' ' + Config.COMMENT_FLAG[2]
    else:
        content_prefix = Config.COMMENT_FLAG
    
    if Config.TYPE in FILE_INFO.keys():
        file_info = FILE_INFO[Config.TYPE]

    date = content_prefix + ' Date: ' + datetime.datetime.now().ctime() + '\n'
    author = content_prefix + ' Author: ' + Config.AUTHOR + '\n'
    
    
    header = header_start + file_info + date + author + header_end
    return header

# 生成文件初始模板内容
def generateNewFormat():
    return FILE_FORMAT[Config.TYPE]

def stamp(filename, type=""):
    if len(filename) <= 0:
        log.notice("no filename, please specify a filename")
        return
    # 从扩展名读取文件类型
    splited_filename = filename.split('.')
    if len(splited_filename) < 2:
        log.warn("filename has no extension, can't decide file type")
    else:
        file_ext = splited_filename[-1]
        Config.TYPE = file_ext
    if Config.TYPE in MULTILINE_COMMENT_FLAG:
        Config.isMultilineComment = True
        Config.COMMENT_FLAG = MULTILINE_COMMENT_FLAG[Config.TYPE]
    elif Config.TYPE in COMMENT_FLAG.keys():
        Config.COMMENT_FLAG = COMMENT_FLAG[Config.TYPE]
    else:
        Config.COMMENT_FLAG = ""
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
    log.notice("%s stamped"%(filename))
    
def main():
    raw_args, options = op.get_options_v2(sys.argv, ['h', 'list'])
    
    if 'list' in options.keys():
        log.notice("supported file type:")
        i = 1
        for file_type in COMMENT_FLAG.keys():
            log.notice("%d. %s"%(i, file_type))
            i += 1
        return
    
    if 'h' in options.keys() or len(raw_args) == 0:
        log.notice(USAGE)
        return
    
    for item in raw_args:
        stamp(item)

if __name__ == '__main__':
    main()
    



