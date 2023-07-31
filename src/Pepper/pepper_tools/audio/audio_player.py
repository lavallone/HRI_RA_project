import qi
import argparse
import sys
import os
import time

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--afile", type=str, help="Audio file to play")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    afile = args.afile

    #Starting application
    try:
        connection_url = "tcp://" + pip + ":" + str(pport)
        print "Connecting to ",	connection_url
        app = qi.Application(["Memory Write", "--qi-url=" + connection_url ])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session
    
    #Starting services
    ap_service = session.service("ALAudioPlayer")

    try:
        #Loads a file and launchs the playing 5 seconds later
        fileId = ap_service.loadFile(os.path.abspath(afile))
        fileLength =ap_service.getFileLength(fileId)
        print 'Playing '+afile+'. Duration: '+ str(fileLength) +' secs. Press Ctrl+C to stop'
        ap_service.play(fileId, _async = True)
        time.sleep(fileLength)
    except KeyboardInterrupt:
        ap_service.stopAll()
        print('Quitting')
        sys.exit(0)


if __name__ == "__main__":
    main()
