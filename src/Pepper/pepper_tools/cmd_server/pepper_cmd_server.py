#!/usr/bin/env python

import sys
import os
import socket
import importlib
from threading import Thread

import re
import argparse
import qi
import pepper_cmd
from pepper_cmd import *

status = "Idle"             # robot status sent to websocket

robot = pepper_cmd.robot

def exec_fn(fn,vd):
    largs = []
    for i in range(1,len(vd)):
        if (vd[i]!=''):
            largs += [ vd[i] ]
    print 'Executing ',fn,' with args ',largs
    try:
        if (len(largs)==0):
            fn()
        elif (len(largs)==1):
            if (largs[0][0]=='"'):
                print "string argument"
                fn(largs[0])
            else:
                fn(int(largs[0]))
        elif (len(largs)==2):
            fn(int(largs[0]),int(largs[1]))
    except:
        print "ERROR: executing",fn," with args ",largs


def exec_cmd(data):
    print "received command:", data
    vd = re.split('[(,)_]',data)
    try:
        fn = getattr(pepper_cmd, vd[0])
    except:
        print "ERROR: function",vd[0],"not found"
        fn = None
    if (not fn is None):
        exec_fn(fn,vd)



def run_code(code):
    global status
    if (code is None):
        return
    print("=== Start code run ===")
    #code = beginend(code)
    print("Executing")
    print(code)
    try:
        status = "Executing program"
        exec(code)
    except Exception as e:
        print("CODE EXECUTION ERROR")
        print e
    status = "Idle"
    print("=== End code run ===")



def start_server(TCP_PORT):

    TCP_IP = ''
    BUFFER_SIZE = 200

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP,TCP_PORT))
    s.listen(1)

    run=True

    while run:
        print "Robot Program Server: waiting for connections port", TCP_PORT
        connected = False
        conn = None
        try:
            conn, addr = s.accept()
            print "Connection address:", addr
            connected = True
        except KeyboardInterrupt:
            print "User quit."
            run = False

        while (run and connected):
            data = ''
            while (run and connected and ((data=='') or (data[0]!='*' and data[0]!='[' and (not '###ooo###' in data)))):
                try:
                    d = conn.recv(BUFFER_SIZE)
                except:
                    print "Pepper Cmd Server: connection closed."
                    connected = False
                    break
                if (d==''):
                    break
                data = data + d
                #print "Received partial data: ",data

            if (not connected):
                break
            if (not data or data==''):
                break

            print "Received: ",data
            conn.send("OK\n")

            new_version = True
            if (new_version):
                if (status=='Idle'):
                    t = Thread(target=run_code, args=(data,))
                    t.start()
            else:
                # old version
                vdata = re.split("[\r\n;]",data)
                for i in range(0,len(vdata)):
                    if (vdata[i]=="quit"):
                        connected=False
                        break
                    else:
                        com = vdata[i].strip()
                        if (len(com)>0):
                            exec_cmd(com)

        if (conn is not None):
            conn.close()
        print "Closed connection"




def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
    #                    help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    #parser.add_argument("--pport", type=int, default=9559,
    #                    help="Naoqi port number")
    parser.add_argument("--serverport", type=int, default=5000,
                        help="Server port")

    args = parser.parse_args()
    #pip = args.pip
    #pport = args.pport
    #server_port = args.serverport 

    #Starting application
    #try:
    #    connection_url = "tcp://" + pip + ":" + str(pport)
    #    app = qi.Application(["Program server", "--qi-url=" + connection_url ])
    #except RuntimeError:
    #    print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
    #           "Please check your script arguments. Run with -h option for help.")
    #    sys.exit(1)

    #app.start()
    #pepper_cmd.session = app.session

    start_server(args.serverport)
    


if __name__ == "__main__":
    main()


