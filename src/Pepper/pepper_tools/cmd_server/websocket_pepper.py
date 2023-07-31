# http://www.html.it/pag/53419/websocket-server-con-python/
# sudo -H easy_install tornado

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import time
import argparse
import qi
from threading import Thread

#from dummy_robot import begin,end,forward,backward,left,right

#import sys
#sys.path.append('../program')

import pepper_cmd
from pepper_cmd import *

# Global variables

websocket_server = None     # websocket handler
run = True                  # main_loop run flag
server_port = 9020          # web server port
code = None
status = "Idle"             # robot status sent to websocket

session = None
tablet_service = None
webview = "http://198.18.0.1/apps/spqrel/index.html"

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

# Websocket server handler

class MyWebSocketServer(tornado.websocket.WebSocketHandler):

    def open(self):
        global websocket_server, run
        websocket_server = self
        print('New connection')
       
    def on_message(self, message):
        global code, status
        if (message=='stop'):
            print('Stop code and robot')
            robot_stop_request()
        else:
            print('Code received:\n%s' % message)
            if (status=='Idle'):
                t = Thread(target=run_code, args=(message,))
                t.start()
            else:
                print('Program running. This code is discarded.')
        self.write_message('OK')
  
    def on_close(self):
        print('Connection closed')
  
    def on_ping(self, data):
        print('ping received: %s' %(data))
  
    def on_pong(self, data):
        print('pong received: %s' %(data))
  
    def check_origin(self, origin):
        #print("-- Request from %s" %(origin))
        return True


# Touchscreen callback

# function called when the signal onTouchDown is triggered
def onTouched(x, y):
    global session,tablet_service
    print "coordinates are x: ", x, " y: ", y
    al_service = session.service("ALAutonomousLife")
    if (al_service.getState()!='disabled'):
        tablet_service.showWebview(webview)

# Hand touch callback

def rhTouched(value):
    global session,tablet_service
    print "Right Hand value subscriber=",value
    #al_service = session.service("ALAutonomousLife")
    #if (al_service.getState()!='disabled'):
    if value==1.0:
        tablet_service.showWebview(webview)



# Main loop (asynchrounous thread)

def main_loop(data):
    global run, websocket_server, status, tablet_service
    while (run):
        time.sleep(1)
        #if (run and not websocket_server is None):
            #try:
                #websocket_server.write_message(status)
                #print(status)
            #except tornado.websocket.WebSocketClosedError:
                #print('Connection closed.')
                #websocket_server = None

    print("Main loop quit.")


           

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



# Main program

def main():
    global run

    # Run main thread
    t = Thread(target=main_loop, args=(None,))
    t.start()

    # Run robot
    begin()

    # Run web server
    application = tornado.web.Application([
        (r'/websocketserver', MyWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(server_port)
    print("%sWebsocket server listening on port %d%s" %(GREEN,server_port,RESET))

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print(" -- Keyboard interrupt --")

    # Quit
    end()

    if (not websocket_server is None):
        websocket_server.close()
    print("Web server quit.")
    run = False    
    print("Waiting for main loop to quit...")


def main_OLD():
    global run,session,tablet_service

    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--serverport", type=int, default=9000,
                        help="Server port")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    server_port = args.serverport 

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["Websocket server", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session
    pepper_cmd.session = app.session
    tablet_service = app.session.service("ALTabletService")

    memory_service  = session.service("ALMemory")

    #Tablet touch (does not forward signal to other layers)
    #idTTouch = tablet_service.onTouchDown.connect(onTouched)

    #subscribe to any change on "HandRightBack" touch sensor
    rhTouch = memory_service.subscriber("HandRightBackTouched")
    idRHTouch = rhTouch.signal.connect(rhTouched)


    # Run main thread
    t = Thread(target=main_loop, args=(None,))
    t.start()

    # Run robot
    begin()

    # Run web server
    application = tornado.web.Application([
        (r'/websocketserver', MyWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(server_port)
    print("%sWebsocket server listening on port %d%s" %(GREEN,server_port,RESET))
#    tablet_service.showWebview(webview)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print(" -- Keyboard interrupt --")

    # Quit
    end()

    if (not websocket_server is None):
        websocket_server.close()
    print("Web server quit.")
    run = False    
    print("Waiting for main loop to quit...")



if __name__ == "__main__":
    main()

