import sys
import time
import argparse
import os
import qi

from naoqi import ALProxy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--enable", type=int, default=1,
                        help="(0=deactivate, 1=activate)")
    
    args = parser.parse_args()

    #Starting application
    try:
        connection_url = "tcp://" + args.pip + ":" + str(args.pport)
        app = qi.Application(["Behavior ", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.pip + "\" on port " + str(args.pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()

    enable = args.enable
    
    bm_service = app.session.service("ALBackgroundMovement")
    bm_service.setEnabled(enable)

   	ba_service = app.session.service("ALBasicAwareness")
    ba_service.setEnabled(enable)

    sm_service = app.session.service("ALSpeakingMovement")
    sm_service.setEnabled(enable)
    
if __name__ == "__main__":
    main()

