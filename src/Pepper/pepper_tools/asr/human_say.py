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
    parser.add_argument("--sentence", type=str, default="hello",
                        help="Sentence said by human")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["HumanSay", "--qi-url=" + connection_url ])
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

    tm = int(time.time())  # does not work with float!!!
    memory_service.raiseEvent(fakeASRevent, args.sentence)
    memory_service.insertData(fakeASRkey, args.sentence)
    memory_service.insertData(fakeASRtimekey, tm)

    print("Human Say: '%s' at time %d" %(args.sentence,tm))

if __name__ == "__main__":
    main()
