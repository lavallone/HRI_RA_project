#http://doc.aldebaran.com/2-5/naoqi/motion/control-walk-api.html

import qi
import argparse
import sys
import time
import math
import os

motion_service = None

def init():
    global motion_service

    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    print "Connecting to tcp://" + pip + ":" + str(pport)

	#Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["Move", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    #Starting services
    motion_service = session.service("ALMotion")



def setSpeed(lin_vel,ang_vel,dtime):
    global motion_service
    motion_service.move(lin_vel,0,ang_vel)
    time.sleep(dtime)
    motion_service.stopMove()


def square(r):
    if (r>0.1):
        print 'Square ',r
        v = 0.3
        w = 0.7
        for i in range(0,4):
            setSpeed(v,0,r/v)
            setSpeed(0,w,(math.pi/2)/w)


def circle(r):
    if (r>0.1):
        print 'Circle ',r
	v = 0.3
	dt = 2*math.pi*r/v
	w = 2*math.pi/dt # = v/r
	setSpeed(v,w,dt)


def forward(r=1):
    print 'Forward ',r
    s = 0.5*r
    v = 0.2
    setSpeed(v,0,abs(s/v))

def backward(r=1):
    print 'Backward ',r
    s = 0.5*r
    v = -0.2
    setSpeed(v,0,abs(s/v))

def left(r=1):
    print 'Left ',r
    s = (math.pi/2)*r
    w = 0.5
    setSpeed(0,w,abs(s/w))

def right(r=1):
    print 'Right ',r
    s = (math.pi/2)*r
    w = -0.5
    setSpeed(0,w,abs(s/w))




def main():
    
    init()

    forward()
    left()
    right(2)
    left()
    backward()

    #square(0.5)
    #circle(0)



if __name__ == "__main__":
    main()

