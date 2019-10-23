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

def main():
    if len(sys.argv) < 2:
        print(usage)

    function = sys.argv[1]
    if function == "receive":
        receiveFile()
    elif function == "send":
        sendFile("test.txt","192.168.1.1", 19999)
    
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
        print("client disconnected");
   
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
