#! /usr/bin/env python

#http://doc.aldebaran.com/2-5/naoqi/motion/tools-general-api.html

"""Example: Use getSensorNames Method"""

import qi
import argparse
import sys
import os

def main(session):
    """
    This example uses the getSensorNames method.
    """
    # Get the service ALMotion.

    motion_service  = session.service("ALMotion")

    # Example showing how to get the list of the sensors
    sensorList = motion_service.getSensorNames()
    for sensor in sensorList:
        print sensor


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    #Start working session
    session = qi.Session()
    try:
        session.connect("tcp://" + pip + ":" + str(pport))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    main(session)
