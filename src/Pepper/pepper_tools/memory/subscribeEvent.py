
import qi
import argparse
import sys
import os

def onEvent(value):
    print "value=",value

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--event", type=str, default="event_test",
                        help="name of the event to subscribe")
    
    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    event = args.event

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
    subscriber = memory_service.subscriber(event)
    idEvent = subscriber.signal.connect(onEvent)
    
    #Program stays at this point until we stop it
    app.run()

    #Disconnecting callbacks
    subscriber.signal.disconnect(idEvent)
    
    print "Finished"


if __name__ == "__main__":
    main()
