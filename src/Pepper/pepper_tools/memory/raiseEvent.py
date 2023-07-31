


import qi
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--event", type=str, default="event_test",
                        help="name of the event to raise")
    parser.add_argument("--data", type=str, default="data_event_test",
                        help="data to send")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    event = args.event
    data = args.data
    
    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        app = qi.Application(["ReactToTouch", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

    #Starting services
    memory_service  = session.service("ALMemory")
      
    #subscribe to any change on any touch sensor
    memory_service.raiseEvent(event, data)
    
    print "Finished"


if __name__ == "__main__":
    main()
