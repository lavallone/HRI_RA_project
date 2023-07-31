#!/bin/bash

# Use  ./run.bash [version]

IMAGENAME=pepper-hri

VERSION=latest
if [ ! "$1" == "" ]; then
  VERSION=$1
fi

# change settings here if needed
CAMERA_DEVICE=/dev/video0
PEPPER_TOOLS_HOME=$HOME/Desktop/HRI_RA_project/src/Pepper/pepper_tools
MODIM_HOME=$HOME/Desktop/HRI_RA_project/src/modim
PLAYGROUND_FOLDER=$HOME/Desktop/HRI_RA_project/pepper_interaction


echo "Running image $IMAGENAME:$VERSION ..."

if [ -f $CAMERA_DEVICE ]; then
  echo "Camera device $CAMERA_DEVICE enabled"
  CAMERA_DEVICE_STR="--device=$CAMERA_DEVICE"
fi

if [ -d /run/user/$(id -u)/pulse ]; then
  AUDIO_STR="--device=/dev/snd \
           -v /run/user/$(id -u)/pulse:/run/user/1000/pulse \
           -v $HOME/.config/pulse/cookie:/opt/config/pulse/cookie"
  echo "Audio support enabled"
fi

chmod go+rw ~/.config/pulse/cookie # this file needed by docker user


docker run -it -d \
    --name pepperhri --rm \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $HOME/.Xauthority:/home/robot/.Xauthority:rw \
    -e DISPLAY=$DISPLAY \
    --privileged \
    --net=host \
    $CAMERA_DEVICE_STR \
    $AUDIO_STR \
    -v $PLAYGROUND_FOLDER:/home/robot/playground \
    -v $PEPPER_TOOLS_HOME:/home/robot/src/pepper_tools \
    -v $MODIM_HOME:/home/robot/src/modim \
    -v $HOME/.qibullet:/home/robot/.qibullet \
    -e MODIM_HOME=/home/robot/src/modim \
    -e MODIM_APP=/home/robot/playground \
    $IMAGENAME:$VERSION


