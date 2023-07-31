import qi
import argparse
import sys
import time
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--values", type=str, default='[0.00, -0.21, 1.55, 0.13, -1.24, -0.52, 0.01, 1.56, -0.14, 1.22, 0.52, -0.01]',
                        help="Joint values")
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    values = eval(args.values)

    #Starting session
    session = qi.Session()
    try:
        session.connect("tcp://" + pip + ":" + str(pport))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)


    leds_service = session.service("ALLeds")


    time.sleep(3)

    leds_service.on('FaceLeds')

    sys.exit(1)
    

    leds_service.randomEyes(5)
    time.sleep(1)
    leds_service.rasta(5)
    time.sleep(1)
    leds_service.rotateEyes(0x00802020, 1, 5)
    time.sleep(1)
    leds_service.off('AllLeds')
    time.sleep(1)
    leds_service.on('AllLeds')
    time.sleep(1)
    leds_service.reset('AllLeds')

if __name__ == "__main__":

    main()



