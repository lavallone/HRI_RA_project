# Touch simulation using memory keys
#
# Device/SubDeviceList/Head/Touch/Middle/Sensor/Value
# Device/SubDeviceList/LHand/Touch/Back/Sensor/Value
# Device/SubDeviceList/RHand/Touch/Back/Sensor/Value

import qi
import argparse
import sys
import time
import threading
import os


memkey = {
    'HeadMiddle': 'Device/SubDeviceList/Head/Touch/Middle/Sensor/Value' ,
    'LHand':      'Device/SubDeviceList/LHand/Touch/Back/Sensor/Value' ,
    'RHand':      'Device/SubDeviceList/RHand/Touch/Back/Sensor/Value' }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--sensor", type=str, default="HeadMiddle",
                        help="Sensor: HeadMiddle, LHand, RHand")
    parser.add_argument("--duration", type=float, default=3.0,
                        help="Duration of the event")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["TouchSim", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    #Starting services
    memory_service  = session.service("ALMemory")
    
    try:
        mkey = memkey[args.sensor]
        print("Touching %s ..." %args.sensor)
        memory_service.insertData(mkey,1.0)
        time.sleep(args.duration)
        memory_service.insertData(mkey,0.0)
        print("Touching %s ... done" %args.sensor)
    except:
        print("ERROR: Sensor %s unknown" %args.sensor)

if __name__ == "__main__":
    main()
