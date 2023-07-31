#! /usr/bin/env python

#http://doc.aldebaran.com/2-5/naoqi/motion/control-cartesian-api.html
"""Example: Use getPosition Method"""

import qi
import argparse
import sys
import motion
import os


frames = ["Torso", "World", "Robot"]

def main(session, sensor, frame):
    """
    This example uses the getPosition method.
    """
    # Get the service ALMotion.

    motion_service  = session.service("ALMotion")

    # Example showing how to get the position of the top camera
    name            = sensor
    useSensorValues = True
    result          = motion_service.getPosition(name, frame, useSensorValues)

    print "Position of", name, " in frame", frames[frame] , " is:"
    print "Translation (x,y,z) = [", result[0],",", result[1],",", result[2],"]"
    print "Rotation    (x,y,z) = [", result[3],",", result[4],",", result[5],"]"

    print "Transformation: "
    result = motion_service.getTransform(name, frame, useSensorValues)
    for i in range(0, 4):
        for j in range(0, 4):
            print result[4*i + j],
        print ''
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--sensor", type=str, default="CameraTop",
                        help="Sensor name. To check possible names use getSensorNames.py.")
    parser.add_argument("--frame", type=int, default=2,
                        help="Frame with respect to which express position: (0 = Torso, 1 = World, 2 = Robot)")

    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    sensor = args.sensor
    frame = args.frame
    
    #Start working session
    session = qi.Session()
    try:
        session.connect("tcp://" + pip + ":" + str(pport))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
        
    main(session, sensor, frame)
