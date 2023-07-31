#http://doc.aldebaran.com/2-5/naoqi/audio/alspeechrecognition-api.html
import qi
import argparse
import sys
import os

def onWordRecognized(value):
    print "value=",value


    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    
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
    asr_service = session.service("ALSpeechRecognition")
    asr_service.setLanguage("English")

    memory_service  = session.service("ALMemory")

    #establishing test vocabulary
    vocabulary = ["yes", "no", "please", "hello", "goodbye", "hi, there", "go to the kitchen"]
    asr_service.setVocabulary(vocabulary, False)

    # Start the speech recognition engine with user Test_ASR
    asr_service.subscribe("Test_ASR")
    print 'Speech recognition engine started'

    #subscribe to event WordRecognized
    subWordRecognized = memory_service.subscriber("WordRecognized")
    idSubWordRecognized = subWordRecognized.signal.connect(onWordRecognized)

    #let it run
    app.run()

    #Disconnecting callbacks and subscribers
    asr_service.unsubscribe("Test_ASR")
    subWordRecognized.signal.disconnect(idSubWordRecognized)
    

if __name__ == "__main__":
    main()
