import qi
import argparse
import sys
import time
import os


jointsNames = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]

#joint limits taken from http://doc.aldebaran.com/2-5/family/pepper_technical/joints_pep.html
jointLimits ={'HeadYaw': (-2.0857, 2.0857),
              'HeadPitch': (-0.7068, 0.6371),
              'LShoulderPitch': (-2.0857, 2.0857),
              'LShoulderRoll': (0.0087, 1.5620),
              'LElbowYaw': (-2.0857, 2.0857),
              'LElbowRoll': (-1.5620, -0.0087),
              'LWristYaw': (-1.8239, 1.8239),
              'RShoulderPitch': (-2.0857, 2.0857),
              'RShoulderRoll': (-1.5620, -0.0087),
              'RElbowYaw': (-2.0857, 2.0857),
              'RElbowRoll': (0.0087,1.5620),
              'RWristYaw': (-1.8239, 1.8239)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--value", type=float, default=0.8,
                        help="Stiffness value")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    sval = args.value

    if (sval==None):
        print 'No stiffness value'
        sys.exit(0)

    #Starting session
    session = qi.Session()
    try:
        session.connect("tcp://" + pip + ":" + str(pport))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    print "Set stiffness value: ", sval
    isAbsolute = True

    #Starting services
    motion_service  = session.service("ALMotion")

    
   
    names = ["Head", "LArm", "RArm"]
    stiffnessLists = sval
    timeLists = 1.0
    motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)

    time.sleep(3)

    print motion_service.getSummary()

    #print motion_service.getSummary()

    #names = "Body"
    #stiffnessLists = 1.0
    #timeLists = 1.0
    #motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)

    #time.sleep(3)

    #print motion_service.getSummary()

    #motion_service.angleInterpolation(jointsNames, jointValues, 3.0, isAbsolute)
    
    

if __name__ == "__main__":

    main()

