#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: A Simple class to get & read FaceDetected Events"""

import qi
import time
import sys
import os
import argparse

# Python Image Library
import Image

from naoqi import ALProxy

class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        self.ba_service = session.service("ALBasicAwareness")
        self.ba_service.setEnabled(True)
        self.leds_service = session.service("ALLeds")
        self.leds_service.on('FaceLeds') # reset to white
        # Connect the event callback.
        self.fdsub = self.memory.subscriber("FaceDetected")
        self.ch1 = self.fdsub.signal.connect(self.on_human_tracked)
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        self.face_detection = session.service("ALFaceDetection")
        self.face_detection.subscribe("HumanGreeter")
        self.got_face = False
        self.camProxy = None
        self.savedfaces = []


    def connect_camera(self, ip, port):
        # Connect to camera
        self.camProxy = ALProxy("ALVideoDevice", ip, port)
        resolution = 2    # VGA
        colorSpace = 11   # RGB
        self.videoClient = self.camProxy.subscribe("vision_faceDetection", resolution, colorSpace, 5)


    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        faceID = -1

        if value == []:  # empty value when the face disappears
            self.got_face = False
            # white face leds
            self.leds_service.on('FaceLeds')

        else:
            # green face leds
            self.leds_service.off('LeftFaceLedsRed')
            self.leds_service.off('LeftFaceLedsBlue')
            self.leds_service.off('RightFaceLedsRed')
            self.leds_service.off('RightFaceLedsBlue')

            if not self.got_face:  # only the first time a face appears

                self.got_face = True
                print "I saw a face!"
                #self.tts.say("Hello, you!")
                # First Field = TimeStamp.
                timeStamp = value[0]
                print "TimeStamp is: " + str(timeStamp)

                # Second Field = array of face_Info's.
                faceInfoArray = value[1]
                for j in range( len(faceInfoArray)-1 ):
                    faceInfo = faceInfoArray[j]

                    # First Field = Shape info.
                    faceShapeInfo = faceInfo[0]

                    # Second Field = Extra info (empty for now).
                    faceExtraInfo = faceInfo[1]

                    faceID = faceExtraInfo[0]

                    #print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
                    #print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
                    #print "Face Extra Infos :" + str(faceExtraInfo)
                    #print "Face ID: %d" %faceID

        if self.camProxy!=None and faceID>=0 and faceID not in self.savedfaces:
            # Get the image 
            img = self.camProxy.getImageRemote(self.videoClient)

            # Get the image size and pixel array.
            imageWidth = img[0]
            imageHeight = img[1]
            array = img[6]

            # Create a PIL Image from our pixel array.
            im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

            # Save the image.
            fname = "face_%03d.png" %faceID
            im.save(fname, "PNG")
            print "Image face %d saved." %faceID

            self.savedfaces.append(faceID)


    def close(self):
        self.face_detection.unsubscribe("HumanGreeter")
        self.camProxy.unsubscribe(self.videoClient)
        self.fdsub.signal.disconnect(self.ch1)
        self.ba_service.setEnabled(False)
        self.leds_service.on('FaceLeds') # reset to white


    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting HumanGreeter"
        try:
            while True:
                #val = self.memory.getData('FaceDetection/FaceDetected')
                #if len(val)>0:
                #    print('Memory value %r' %val)
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping all behaviors"
            self.close()
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.connect_camera(args.ip, args.port)
    human_greeter.run()

