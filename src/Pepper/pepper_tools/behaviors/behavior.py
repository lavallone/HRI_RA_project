# -*- encoding: UTF-8 -*- 

import sys
import time
import argparse
import os
import qi

from naoqi import ALProxy

def executeBehavior(beh_service, behaviorName):
  if (behaviorName is None):
    behaviorName = ".lastUploadedChoregrapheBehavior/behavior_1"

  # run the behaviot
  launchAndStopBehavior(beh_service, behaviorName)

  #add as a default behavior 
  #defaultBehaviors(beh_service, behaviorName)


def stopBehavior(beh_service, behaviorName):
  # Stop the behavior.
  if (beh_service.isBehaviorRunning(behaviorName)):
    beh_service.stopBehavior(behaviorName)
    time.sleep(1.0)
  else:
    print "Behavior is already stopped."


def getBehaviors(beh_service):
  ''' Know which behaviors are on the robot '''

  names = beh_service.getInstalledBehaviors()
  print "Behaviors on the robot:"
  print names

  names = beh_service.getDefaultBehaviors()
  print "Default behaviors:"
  print names

  names = beh_service.getRunningBehaviors()
  print "Running behaviors:"
  print names


def launchAndStopBehavior(beh_service, behaviorName):
  ''' Launch and stop a behavior, if possible. '''

  # Check that the behavior exists.
  if (beh_service.isBehaviorInstalled(behaviorName)):

    # Check that it is not already running.
    if (not beh_service.isBehaviorRunning(behaviorName)):
      # Launch behavior. This is a blocking call, use post if you do not
      # want to wait for the behavior to finish.
      beh_service.startBehavior(behaviorName)
      #time.sleep(10)
    else:
      print "Behavior is already running."

  else:
    print "Behavior not found."
    return

  #names = beh_service.getRunningBehaviors()
  #print "Running behaviors:"
  #print names


  #names = beh_service.getRunningBehaviors()
  #print "Running behaviors:"
  #print names


def defaultBehaviors(beh_service, behaviorName):
  ''' Set a behavior as default and remove it from default behavior. '''

  # Get default behaviors.
  names = beh_service.getDefaultBehaviors()
  print "Default behaviors:"
  print names

  # Add behavior to default.
  beh_service.addDefaultBehavior(behaviorName)

  names = beh_service.getDefaultBehaviors()
  print "Default behaviors:"
  print names

  # Remove behavior from default.
  beh_service.removeDefaultBehavior(behaviorName)

  names = beh_service.getDefaultBehaviors()
  print "Default behaviors:"
  print names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pip", type=str, default=os.environ['PEPPER_IP'],
                        help="Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--pport", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--start", type=str, default=None, help="start behavior")
    parser.add_argument("--stop", type=str, default=None, help="stop behavior")
    parser.add_argument('--list', help='List available behaviors', action='store_true')

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

    beh_service = app.session.service("ALBehaviorManager")

    if (args.list):
        getBehaviors(beh_service)
    elif (args.start is not None):
        executeBehavior(beh_service,args.start)
    elif (args.stop is not None):
        stopBehavior(beh_service,args.stop)

if __name__ == "__main__":
    main()

