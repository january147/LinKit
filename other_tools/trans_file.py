#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Sat Oct 19 20:45:17 2019
# Author: January

import socket
import sys


usage='''
trans_file receive [-p <port>] [-o <filename>]
trans_file send -f <file> -d <ip> [-p <port>]
'''

class Command:
    S_NULL = 'null'
    S_RECEIVING = 'receiving'
    S_OK = 'ok'

    def __init__(self):
        self.values = dict()
        self.status = Command.S_NULL
        self.raw_cmd = ""
        self.split_raw_cmd = None

    # You can call receiveCmd several times to receive a complete cmd.
    def receiveCmd(self, cmd_data):
        if self.status == Command.S_OK:
            raise RuntimeError('No more data needed')
        if self.status == Command.S_NULL and cmd_data[0] != "^":
            raise RuntimeError("invalid cmd")
        self.raw_cmd += cmd_data
        if self.raw_cmd[-1] == "$":
            self.status = Command.S_OK
            return True
        else:
            self.status = Command.S_RECEIVING
            return False 

    def parseCmd(self):
        self.split_raw_cmd = self.raw_cmd.strip("^$").split("/")
        for key_value in self.split_raw_cmd:
            key, value = key_value.split(":")
            self.values[key] = value


def main():
    if len(sys.argv) < 2:
        print(usage)

    function = sys.argv[1]
    if function == "receive":
        receiveFile()
    elif function == "send":
        sendFile("test.txt","192.168.1.1", 19999)


def protocol_test():
    listen_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_s.bind(('0.0.0.0', 9999))
    listen_s.listen(2)
    while True:
        session_s, addr = listen_s.accept()
        print("connected with " + str(addr))
        
    
def receiveFile():
    listen_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_s.bind(("0.0.0.0", 19999))
    listen_s.listen(4)
    print("waiting for client...")
    while True:
        session_s, addr = listen_s.accept()
        print("connected with " + str(addr))
        received_file = open("received_file", "wb")
        while True:
            data = session_s.recv(4096)
            if len(data) == 0:
                break
            received_file.write(data)
        received_file.close()
        session_s.close()
        print("client disconnected")
   
    listen_s.close()

def sendFile(file_path, ip, port):
    session_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    session_s.connect((ip, port))
    sending_file = open(file_path, 'rb')
    while True:
        data = sending_file.read(4096)
        if len(data) <= 0:
            break
        session_s.send(data)
    
    sending_file.close()
    session_s.close()




if __name__ == "__main__":
    main()
