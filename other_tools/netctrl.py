#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Tue Jul 30 13:35:45 2019
# Author: January

import random
import hashlib
import requests
import time
import re
import sys
import logging
import _thread
import os
import random

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger()

mac_filter_url = "http://192.168.1.1/getpage.gch?pid=1002&nextpage=sec_macfilter_conf_t.gch"

usage="netctrl.py healthy_mode [开启时间] [休息时间] [总时间]"

interacive_help = '''bl 查看当前黑名单
set on|off 打开或关闭网络
add name|mac 添加一个设备到黑名单
rm <index> 删除黑名单中第index个设备'''

action_type = {
    "request" : "basic_apply",
    "delete" : "delete",
    "add" : "new"
}

black_mode = {
    "off" : "0",
    "on" : "1"
}

mac_filter_setting = {
    "IF_ACTION" : "basic_apply",
    "IF_ERRORSTR" : "SUCC",
    "IF_ERRORPARAM" : "SUCC",
    "IF_ERRORTYPE" : "-1",
    "IF_INDEX" : "-1",
    "IF_INSTNUM" : "0",
    "BlackModeset" : "1",
    "ZTE" : "1",
    "BlackMode" : "", 
    "MacAddr" : "",
    "_SESSION_TOKEN" : ""
}

mac_name = {
    "54:04:a6:b1:2f:23" : "home_pc",
    "3c:0c:db:9a:af:d2" : "tv",
    "70:11:24:1f:f8:41" : "ipad"
}

name_mac = {
    "home_pc" : "54:04:a6:b1:2f:23",
    "tv" : "3c:0c:db:9a:af:d2",
    "ipad" : "70:11:24:1f:f8:41"
}

def get_options(args, option_list:list):
    arg_p = 1
    total_arg = len(args)
    options = {}
    raw_arg = []
    options_with_arg = []
    accpet_all = False
    for i in range(len(option_list)):
        option_description = option_list[i]
        if option_description == ':':
            accpet_all = True
            continue
        if option_description[-1] == ':':
            option = option_description[:-1]
            options_with_arg.append(option)
            option_list[i] = option
    while arg_p < total_arg:
        arg = args[arg_p]
        if arg.startswith('--'):
            name = arg[2:]
            if not accpet_all and name not in option_list:
                print("invalid option '%s', pos '%d'"%(name, arg_p))
                exit(1)
            if name not in options_with_arg:
                options[name] = ''
            else:
                arg_p += 1
                if arg_p >= len(args) or args[arg_p].startswith('-'):
                    print("option '%s' requires an argument, pos %d"%(name, arg_p))
                    exit(1)
                value = args[arg_p]
                options[name] = value
        elif arg.startswith('-'):
            names = arg[1:]
            if len(names) <= 1:
                name_likely_with_arg = names
            else:
                for name in names[:-1]:
                    if not accpet_all and name not in option_list:
                        print("invalid option '%s', pos %d"%(name, arg_p))
                        exit(1)
                    if name in options_with_arg:
                        print("option '%s' requiring an argument can be put between options, pos %d"%(name, arg_p))
                        exit(1)
                    options[name] = ''
                name_likely_with_arg = names[-1]
            if not accpet_all and name_likely_with_arg not in option_list:
                print("invalid option '%s', pos %d"%(name_likely_with_arg, arg_p))
                exit(1)
            if name_likely_with_arg not in options_with_arg:
                options[name_likely_with_arg] = ''
            else:
                arg_p += 1
                if arg_p >= len(args) or args[arg_p].startswith('-'):
                    print("option '%s' requires an argument, pos %d"%(name_likely_with_arg, arg_p))
                    exit(1)
                value = args[arg_p]
                options[name_likely_with_arg] = value
        else:
            raw_arg.append(arg)
        arg_p += 1

    return (raw_arg, options)

def passwordSHA256(password):
    plain_pswd = password
    pwd_random = '62893628'
    sha256 = hashlib.sha256()
    sha256.update(str.encode(plain_pswd + pwd_random))
    return sha256.digest().decode(encoding="utf8")

def generate_mac_list(mac_list:list):
    mac_list_dict = {}
    for i in range(len(mac_list)):
        mac_list_dict["BlackMode%d"%(i)] = "1"
        mac_list_dict["MacAddr%d"%(i)] = mac_list[i]
    return mac_list_dict

def get_login_token(page):
    re_ob = re.search(r'getObj\("Frm_Logintoken"\).value[ ]*=[ ]*"([0-9]+)"', page.text)
    if re_ob == None:
        return None
    return re_ob.groups()[0]

def get_session_token(page):
    re_ob = re.search(r'session_token[ ]*=[ ]*\"([0-9]+)\"', page.text)
    if re_ob == None:
        return None
    return re_ob.groups()[0]

class NetworkCtrl:
    OP_OK = "SUCC"
    def __init__(self):
        self.black_list = []
        self.session = None
        self.is_login = False
        self.session_token = ""
        self.login()

    def login_timeout(self):
        time.sleep(60*3)
        self.is_login = False

    def print_black_list(self):
        print("###########black list#############")
        for i in range(len(self.black_list)):
            mac = self.black_list[i]
            print("%d.\t%10s\t%17s"%(i, mac_name[mac], mac))
        print("############## end ###############")

    def check_login(self):
        if not self.is_login:
            print("Not login")
            return False
        if self.session_token == None:
            print("No session token")
            return False
        return True

    def get_error_info(self, page):
        #err_types = re.findall(r"'IF_ERRORTYPE','(.*)'", page.text)
        err_strs = re.findall(r"'IF_ERRORSTR','(.*)'", page.text)
        if len(err_strs) > 0:
            err = err_strs[-1]
        else:
            err = "SUCC"
        return err

    def login(self):
        if self.is_login:
            return True
        self.session = requests.session()
        try:
            login_page = self.session.get("http://192.168.1.1")
        except Exception as e:
            print(e)
            return False
        frm_login_token = get_login_token(login_page)
        login_data = {
            "Frm_Logintoken" : frm_login_token,
            "Right" : "",
            "Username" : "user",
            "UserRandomNum" : "36735000",
            "Password" : "bdcabb54eb2b72b716e9d15afaf3c907dafacdf580b98493ee6a35fc95bc7f64",
            "action" : "login"
        }
        if frm_login_token == None:
            print("no session token")
        logger.debug("login_token %s"%frm_login_token)
        try:
            result = self.session.post("http://192.168.1.1", data=login_data)
        except Exception as e:
            print(e)
            return False
        if result.status_code == 200 and self.enter_mac_filter_page() == True:
            self.is_login = True
        _thread.start_new_thread(self.login_timeout, ())
        return self.is_login

    def enter_mac_filter_page(self):
        try:
            result = self.session.get(mac_filter_url)
        except Exception as e:
            print(e)
            self.is_login =False
            return False
        self.session_token = get_session_token(result)
        self.update_local_black_list(result)
        if result.status_code != 200 or self.get_error_info(result) != NetworkCtrl.OP_OK:
            print("无法打开mac控制页面")
            return False
        return True

    def update_local_black_list(self, page):
        new_black_list = re.findall(r"(?:[0-9a-fA-F]{2}\\x3a){5}[0-9a-fA-F]{2}", page.text)
        for i in range(len(new_black_list)):
            new_black_list[i] = new_black_list[i].replace("\\x3a", ":")
        self.black_list = new_black_list
        #self.print_black_list()

    def set_black_mode(self, enable):
        if self.check_login() == False:
            return False
        logger.debug("session_token %s"%self.session_token)
        if enable:
            mode = "on"
        else:
            mode = "off"
        mac_filter_setting["BlackModeset"] = black_mode[mode]
        mac_filter_setting["_SESSION_TOKEN"] = self.session_token
        if not enable:
            mac_filter_setting.update(generate_mac_list(self.black_list))
            mac_filter_setting["IF_INSTNUM"] = str(len(self.black_list))
        try:
            result = self.session.post(mac_filter_url, data=mac_filter_setting)
        except Exception as e:
            print(e)
            self.is_login =False
            return False
        self.session_token = get_session_token(result)
        err = self.get_error_info(result)
        if result.status_code != 200 or err != NetworkCtrl.OP_OK:
            print("设置黑名单失败，错误：%s"%(err))
            return False
        # with open("data.html", "wb") as file:
        #     file.write(result.content)
        self.update_local_black_list(result)
        return True

    def add_black_mac(self, mac_addr):
        if self.check_login() == False:
            return False
        logger.debug("session_token %s"%self.session_token)
        mac_filter_setting["IF_ACTION"] = action_type["add"]
        mac_filter_setting["BlackModeset"] = black_mode["on"]
        mac_filter_setting["MacAddr"] = mac_addr
        mac_filter_setting["BlackMode"] = black_mode["on"]
        mac_filter_setting["_SESSION_TOKEN"] = self.session_token
        mac_filter_setting["IF_INSTNUM"] = str(len(self.black_list))
        mac_filter_setting.update(generate_mac_list(self.black_list))
        try:
            result = self.session.post(mac_filter_url, data=mac_filter_setting)
        except Exception as e:
            print(e)
            self.is_login =False
            return False
        self.session_token = get_session_token(result)
        err = self.get_error_info(result)
        if result.status_code != 200 or err != NetworkCtrl.OP_OK:
            print("增加黑名单失败，错误：%s"%(err))
            return False
        # with open("data.html", "wb") as file:
        #     file.write(result.content)
        self.update_local_black_list(result)
        return True

    def rm_black_mac(self, index):
        if self.check_login() == False:
            return False
        logger.debug("session_token %s"%self.session_token)
        mac_filter_setting["IF_ACTION"] = action_type["delete"]
        mac_filter_setting["BlackModeset"] = black_mode["on"]
        mac_filter_setting["_SESSION_TOKEN"] = self.session_token
        mac_filter_setting["IF_INDEX"] = str(index)
        mac_filter_setting["IF_INSTNUM"] = str(len(self.black_list))
        mac_filter_setting.update(generate_mac_list(self.black_list))
        try:
            result = self.session.post(mac_filter_url, data=mac_filter_setting)
        except Exception as e:
            print(e)
            self.is_login =False
            return False
        self.session_token = get_session_token(result)
        # with open("data.html", "wb") as file:
        #     file.write(result.content)
        err = self.get_error_info(result)
        if result.status_code != 200 or err != NetworkCtrl.OP_OK:
            print("删除黑名单失败，错误：%s"%(err))
            return False
        self.update_local_black_list(result)
        return True

def healthy_mode(on=30, off=10, allowed_total=60):
    total_on = 0
    total_off = 0
    nctl = NetworkCtrl()
    print("本次总计可玩%d分钟，每%d分钟休息%d分钟"%(allowed_total, on, off))
    while True:
        try:
            # 开启网络
            if nctl.login() == False or nctl.set_black_mode(False) == False:
                print("Error")
                return
            # 计算时间
            for i in range(on):
                print("目前总计玩了%d分钟，本次还可以玩%d分钟"%(total_on, on - i), end="\r")
                time.sleep(60)
                total_on += 1
                if total_on > allowed_total:
                    nctl.login()
                    if nctl.set_black_mode(True) == False:
                        print("关闭网络失败")
                    print("总时长已到，退出程序")
            # 清除输出
            print("%50s"%(""), end="\r")
            # 关闭网络
            if nctl.login() == False or nctl.set_black_mode(True) == False:
                print("Error")
                return
            # 计时
            for i in range(off):
                print("开始休息了，还有%d分钟"%(off-i), end="\r")
                time.sleep(60)
                total_off += 1
            # 清除输出
            print("%50s"%(""), end="\r")
        except:
            print()
            print("退出healthy mode，共计玩了%d分钟，休息%d分钟"%(total_on, total_off))
            return

def joke():
    nctl = NetworkCtrl()
    while True:
        try:
            nctl.login()
            nctl.set_black_mode(False)
            print("有网了")
            on = random.randint(1, 20)
            print("%d分钟后断网"%(on))
            time.sleep(on * 60)
            nctl.login()
            nctl.set_black_mode(True)
            print("断网了")
            off = random.randint(5, 15)
            print("断网%d分钟"%(off))
            time.sleep(off*60)
        except:
            print("玩笑结束")
            break

class CmdMode:
    def __init__(self):
        self.nctl = NetworkCtrl()

    def run(self):
        nctl = self.nctl
        while True:
            cmd = input(">>>")
            cmd = cmd.split(" ")
            cmd_type = cmd[0]
            arg = cmd[1:]
            if cmd_type == "bl":
                nctl.print_black_list()
            elif cmd_type == "set":
                if len(arg) < 1:
                    continue
                elif arg[0] == "on":
                    nctl.set_black_mode(True)
                elif arg[0] == "off":
                    nctl.set_black_mode(False)
                else:
                    continue
            elif cmd_type == "add":
                if arg[0] in name_mac.keys():
                    nctl.add_black_mac(name_mac[arg[0]])
                else:
                    match = re.match("(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", arg[0])
                    if match == None:
                        print("not valid mac")
                        continue
                    nctl.add_black_mac(arg[0])
            elif cmd_type == "rm":
                try:
                    index = int(arg[0])
                except:
                    print("not valid index")
                nctl.rm_black_mac(index)
            elif cmd_type == "healthy_mode":
                on = 30
                off = 10
                total = 60
                try:
                    on = int(arg[0])
                except:
                    pass
                try:
                    off = int(arg[1])
                except:
                    pass
                try:
                    off = int(arg[2])
                except:
                    pass
                _thread.start_new_thread(os.system, ("deepin-terminal -x %s --healthy_mode %d %d %d"%(os.path.abspath(__file__), on, off, total), ))
            elif cmd_type == "joke":
                print("你开了一个玩笑")
                _thread.start_new_thread(os.system, ("deepin-terminal -x %s --joke"%(os.path.abspath(__file__)), ))
            elif cmd_type == "login":
                nctl.login()
            elif cmd_type == "h":
                print(interacive_help)
            elif cmd_type == "q":
                break

# main
if len(sys.argv) <= 1:
    cmd_mode = CmdMode()
    cmd_mode.run()
else:
    args, options = get_options(sys.argv, ['healthy_mode', 'joke', 'o', 'c'])
    if 'healthy_mode' in options.keys():
        try:
            on = int(args[0])
        except:
            pass
        try:
            off = int(args[1])
        except:
            pass
        try:
            total = int(args[2])
        except:
            pass
        healthy_mode(on, off, total)
    elif "joke" in options.keys():
        joke()
    elif 'o' in options.keys():
        nctl = NetworkCtrl()
        nctl.set_black_mode(False)
    elif 'c' in options.keys():
        nctl = NetworkCtrl()
        nctl.set_black_mode(True)




