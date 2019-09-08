#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Mon Feb 18 22:01:46 2019
# Author: January

import os
import sys
import datetime

USAGE = '[Usage] stamp <filename> [type]'
STAMP = {
    'py' : '#!/usr/bin/python3\n'
           '# -*- coding: utf-8 -*-\n',
    'sh' : '#!/bin/bash\n'
}

class Config(object):
    TYPE = 'py'
    AUTHOR = 'January'
    COMMENT_FLAG = '#'

    @staticmethod
    def config():
        if len(sys.argv) >= 3:
            Config.TYPE = sys.argv[2]

def generateStamp():
    date = Config.COMMENT_FLAG + ' Date: ' + datetime.datetime.now().ctime() + '\n'
    author = Config.COMMENT_FLAG + ' Author: ' + Config.AUTHOR + '\n'
    stamp = STAMP[Config.TYPE] + date + author
    return stamp

def stamp():
    try:
        filename = sys.argv[1]
    except:
        print(USAGE)
        return
    # 从扩展名读取文件类型
    file_ext = filename.split('.')[-1]
    Config.TYPE = file_ext
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
        pass
    new_file.close()
    os.rename(working_filename, filename)
    # 修改权限
    os.system('chmod 755 ' + filename)
    
    
if __name__ == '__main__':
    Config.config()
    stamp()
    



