import pyprind
import sys
import os
import string
import threading
import time
import datetime
import random

#简单封装pyprind
class ProgressBar(object):
    def __init__(self, full=100, title='', type='bar'):
        self.full = full
        self.title = title
        if type == 'bar':
            self.indicator = pyprind.ProgBar(full, title=title)
        else:
            self.indicator == pyprind.ProgPercent(full, title=title)
    def update(self, current_progress):
        last_progress = self.indicator.cnt
        diff = current_progress - last_progress
        if diff > 0:
            self.indicator.update(diff)
    def getProgress(self):
        return self.indicator.cnt
    
    def finish(self):
        if self.indicator.cnt != self.full:
            self.update(self.full)

#运行一个执行时间较长的线程，显示动画以指示正在运行
def user_wait(thread):
    thread.start()
    count = 0
    line_max = 10
    while thread.is_alive():
        print('\b=>', end='')
        sys.stdout.flush()
        count = count + 1
        time.sleep(1)
        if count == line_max:
            print()
            count = 0
    print()

# 打包一个目录，调用了tar命令
def tar(package_name, dir_path):
    cmd = 'tar -czf %s %s'%(package_name, dir_path)
    print(cmd)
    print("tar begin")
    tar_thread = threading.Thread(target=os.system, args=(cmd,))
    user_wait(tar_thread)
    print('tar finish')

# 返回随机字符串
def random_str(str_len = 8):
    result_str = ''.join((random.choice(string.ascii_letters) for i in range(str_len)))
    return result_str

# 返回当前时间
def get_readable_time():
    t = datetime.datetime.now()
    return t.strftime('[%Y-%m-%d %H:%M:%S] ')

# 将字节类型转换成16进制的字符串表示
def bytes2hexstr(data:bytes, prefix:bool=False):
    if prefix:
        result = "0x"
    else:
        result = ""
    for item in data:
        result += "%02x"%(item)
    return result