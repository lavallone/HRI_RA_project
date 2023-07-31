#!/usr/bin/env python

import sys
import os
import socket
import importlib
import re
import argparse
import qi


def start_client(server_ip,server_port,program):

    TCP_IP = ''
    BUFFER_SIZE = 200

    print "Connecting to %s:%d..." %(server_ip,server_port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((server_ip,server_port))

    f = open(program,'r') 
    data = f.read() 
    f.close()

    print "Sending program...",

    s.send(data+ "\n###ooo###\n")

    print(" done")

    data = s.recv(BUFFER_SIZE)

    print "Reply: ",data

    s.close()

    print("Closed connection")




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--serverip", type=str, default='127.0.0.1',
                        help="Server IP address.")
    parser.add_argument("--serverport", type=int, default=5000,
                        help="Server port")
    parser.add_argument("--program", type=str, default="default.py",
                        help="Program file to send")

    args = parser.parse_args()
    server_ip = args.serverip
    server_port = args.serverport 
    program = args.program

    #Starting application
    start_client(server_ip,server_port,program)
    


if __name__ == "__main__":
    main()


