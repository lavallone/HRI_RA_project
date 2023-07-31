# Sonar simulation using memory keys
#
# Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value
# Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value

import qi
import argparse
import sys
import time
import threading
import os


memkey = {
    'SonarFront': 'Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value',
    'SonarBack':  'Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value' }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--sensor", type=str, default="SonarFront",
                        help="Sensor: SonarFront, SonarBack")
    parser.add_argument("--value", type=float, default=0.75,
                        help="Sensor measurement")
    parser.add_argument("--duration", type=float, default=3.0,
                        help="Duration of the event")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["SonarSim", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    #Starting services
    memory_service  = session.service("ALMemory")

    val = None
    try:
        val = float(args.value)
    except:
        print("ERROR: value not numerical")
        return

    try:
        mkey = memkey[args.sensor]
        print("Sonar %s = %f" %(args.sensor,val))
        memory_service.insertData(mkey,val)
        time.sleep(args.duration)
        memory_service.insertData(mkey,0.0)
    except:
        print("ERROR: Sensor %s unknown" %args.sensor)

if __name__ == "__main__":
    main()
