#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Tue Mar  5 14:16:46 2019
# Author: January

########################
##打包你的文件到阿里云
########################
# 需要安装pyprind(进度条)， oss2(阿里云oss python sdk)
# 文件打包压缩tar -czf <压缩包名> <需要打包的目录>
# -c表示打包，-x是解包, -z表示使用gzip压缩

import oss2
import os
import sys
import threading
import time
import datetime
import pyprind
import random
import string
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
from itertools import islice


usage = 'backup2oss -s <backup_dir_path> [-d <remote_dir>]'
custom_config = {
    'id': '',
    'key': '',
    'url': '',
    'bucket': '',
    'remote_dir': '',
    'dir_path' : '',
}

class Jlib():
    # 工具函数
    @staticmethod
    def tar(package_name, dir_path):
        cmd = 'tar -czf %s %s'%(package_name, dir_path)
        print(cmd)
        print("tar begin")
        tar_thread = threading.Thread(target=os.system, args=(cmd,))
        Jlib.user_wait(tar_thread)
        print('tar finish')

    #运行一个执行时间较长的线程，显示动画以指示正在运行
    #工具函数
    @staticmethod
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

    # 工具函数
    # 返回随机字符串
    @staticmethod
    def random_str(str_len = 8):
        result_str = ''.join((random.choice(string.ascii_letters) for i in range(str_len)))
        return result_str

    # 无耦合，返回当前时间
    @staticmethod
    def get_readable_time():
        t = datetime.datetime.now()
        return t.strftime('[%Y-%m-%d %H:%M:%S] ')

    # 读取输入的选项
    @staticmethod
    def get_options():
        options = dict()
        option_name = ''
        no_name_options_count = 0
        waiting_for_value = False
        for item in sys.argv[1:]:
            if(item.startswith('-')):
                option_name = item
                waiting_for_value = True
                options[option_name] = ''
            else:
                if waiting_for_value is True:
                    options[option_name] = item
                else:
                    options[no_name_options_count] = item
                    no_name_options_count = no_name_options_count + 1
        # debug info
        # print(sys.argv)
        return options


#简单封装pyprind
#无外部耦合
class ProgressBar(object):
    def __init__(self, full=100, title=''):
        self.full = full
        self.title = title
        self.indicator = pyprind.ProgBar(full,title=title)
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

class Global(object):
    indicator = ProgressBar()
    
# 代表一个已经打包的目录
class Package(object):
    def __init__(self, dir_path, remote_dir, package_ext='.tar.gz'):
        self.package_name = os.path.basename(dir_path.strip('/')) + package_ext
        self.remote_key = remote_dir+ '/' + self.package_name
        self.dir_path = dir_path
        self.package_path = os.path.abspath(self.package_name)
        self.generate_file()
        self.max_retry = 5
    
    def generate_file(self):
        if os.path.exists(self.package_name):
            print('use existed file \'{filename}\' in current dir'.format(filename=self.package_name))
        else:
            Jlib.tar(self.package_name, self.dir_path)

    def deliver(self, bucket, progress_callback=None):
        for i in range(self.max_retry):
            try:
                oss2.resumable_upload(bucket, self.remote_key, self.package_path, progress_callback=progress_callback)
                Global.indicator.finish()
                os.remove(self.package_path)
                print('%s %s delivered, remote_key is %s'%(Jlib.get_readable_time(), self.package_name, self.remote_key))
                return
            except Exception as e:
                print('upload failed, try again, total try: %d'%(i+1))
                print(repr(e))
                time.sleep(2)
        print('stop trying, please check the error info')


class Backuper():
    option_name = {
        '-s':'dir_path',
        '-d':'remote_dir'
    }
    def __init__(self, config):
        self.config = config
        
    def get_bucket(self):
        auth = oss2.Auth(self.config['id'], self.config['key'] )
        bucket = oss2.Bucket(auth, self.config['url'], self.config['bucket'])
        return bucket
    
    @staticmethod
    def progress_callback(consumed_bytes, total_bytes):
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            Global.indicator.update(rate)
    

    def run(self):
        options = Jlib.get_options()
        if '-s' not in options.keys():
            print(usage)
            return
        for key in options.keys():
            if key in Backuper.option_name.keys():
                key_name = Backuper.option_name[key]
                self.config[key_name] = options[key]

        package = Package(self.config['dir_path'], self.config['remote_dir'])
        package.deliver(self.get_bucket(), Backuper.progress_callback)


if __name__ == "__main__":
    app = Backuper(custom_config)
    app.run()


