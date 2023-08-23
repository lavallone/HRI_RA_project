# coding=utf-8
import qi
import argparse
import sys
import time
import os

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import json
import select
from threading import Thread


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("-robotport", type=int, default=9559,
                        help="Pepper port number")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.robotport

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["HumanRobotInteraction", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    memory_service  = session.service("ALMemory")

    fakeASRkey = 'FakeRobot/ASR'
    fakeASRevent = 'FakeRobot/ASRevent'
    fakeASRtimekey = 'FakeRobot/ASRtime'

    memkey = {
    'SonarFront': 'Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value',
    'SonarBack':  'Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value', 
    'HeadMiddle': 'Device/SubDeviceList/Head/Touch/Middle/Sensor/Value' ,
    'LHand':      'Device/SubDeviceList/LHand/Touch/Back/Sensor/Value' ,
    'RHand':      'Device/SubDeviceList/RHand/Touch/Back/Sensor/Value'
    }

    memkey_transl = {
        'sonarf':'SonarFront',
        'sonarb': 'SonarBack',
        'head': 'HeadMiddle',
        'lhand': 'LHand',
        'rhand': 'RHand'
    }
    sent = 'START'

    #print('To simulate the interaction of the human with Pepper you can write directly what do you want to tell and for the physical reaction'+
    # ' you ahve to use this template: nofsensor_valueofsensor')

    while sent != 'STOP':
        
        sent = raw_input('Human: ')

        split = sent.split(' ')

        if split[0] in     memkey_transl.keys():
            sensor_class = split[0]
            sensor_value = float(split[1])

            if sensor_class in ['sonarf', 'sonarb']:      #== 1 or sensor_class == 2:   #sonar front / sonar back
                print('Type Sensor Input = %s, Sensor Value = %f' %(sensor_class, sensor_value))
                try:
                    mkey = memkey[memkey_transl[sensor_class]]
                    print("Sonar %s = %f" %(mkey, sensor_value))
                    memory_service.insertData(mkey,sensor_value)
                    #time.sleep(args.duration)                      #it is necessary only if we want simulate the value for a determinated time 
                    #memory_service.insertData(mkey,0.0)            #vedere se va bene
                    print(memory_service.getData(mkey,sensor_value))
                except:
                    print("ERROR: Sensor %s unknown" %args.sensor)
            
            else:       #if sensor_class in ['HeadMiddle', 'LHans', 'RHand']:
                try:
                    mkey = memkey[memkey_transl[sensor_class]]
                    print("Touching %s ..." %mkey)
                    memory_service.insertData(mkey,1.0)
                    time.sleep(1)               #touch interaction duration 
                    memory_service.insertData(mkey,0.0)
                    print("Touching %s ... done" %mkey)
                except:
                    print("ERROR: Sensor %s unknown" %args.sensor)
        else:
            tm = int(time.time())
            memory_service.raiseEvent(fakeASRevent, sent)
            memory_service.insertData(fakeASRkey, sent)
            memory_service.insertData(fakeASRtimekey, tm)
            print("Human Say: '%s' " %(sent))


if __name__ == "__main__":
    main()
