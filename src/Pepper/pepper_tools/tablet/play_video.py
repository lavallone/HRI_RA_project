#http://doc.aldebaran.com/2-5/naoqi/core/altabletservice-api.html

import qi
import argparse
import sys
import time
import os

run = False

def onVideoFinished():
    global run
    print "Video play finished."
    run = False

def main():
    global run
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--url", type=str, default="video.mp4",
                        help="video to play (mp4 H264/AAC)")

    args = parser.parse_args()
    pip = args.pip
    pport = args.pport
    weburl = args.url

    #Start working session
    session = qi.Session()
    try:
        session.connect("tcp://" + pip + ":" + str(pport))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + pip + "\" on port " + str(pport) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    tablet_service = session.service("ALTabletService")

    if weburl.startswith('http'):
        strurl=weburl
    else:
        strurl = "http://198.18.0.1/apps/spqrel/%s" %(weburl)
    print "URL: ",strurl

    #strurl = weburl
    tablet_service.playVideo(strurl) # non blocking

    run = True

    

    idVF = tablet_service.videoFinished.connect(onVideoFinished)
    #app.start()

    while (run):
        time.sleep(0.5)

    tablet_service.videoFinished.disconnect(idVF)
    #app.stop()


if __name__ == "__main__":
    main()

