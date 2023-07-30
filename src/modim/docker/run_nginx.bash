#!/bin/bash

HTMLPORT=80

if [ "$1" != "" ]; then
    HTMLPORT=$1
fi

if [ "$MODIM_HOME" = "" ]; then
  MODIM_HOME=$HOME/src/modim
fi

if [ "$MODIM_APP" = "" ]; then
  MODIM_APP=$MODIM_HOME/demo/sample
fi


echo "nginx server running on port ${HTMLPORT}"

docker run -it -d \
    --name nginx --rm \
    -p ${HTMLPORT}:80 \
    -v $MODIM_APP:/usr/share/nginx/html \
    nginx


