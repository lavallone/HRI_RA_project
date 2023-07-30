#!/bin/bash

# Use  ./run.bash [version]

IMAGENAME=modim

VERSION=latest
if [ "$1" != "" ]; then
  VERSION=$1
fi

if [ "$MODIM_HOME" = "" ]; then
  MODIM_HOME=$HOME/src/modim
fi

if [ "$MODIM_APP" = "" ]; then
  MODIM_APP=$MODIM_HOME/demo/sample
fi

echo "Running image $IMAGENAME:$VERSION ..."

docker run -it \
    --name modim --rm -d \
    --net=host \
    -e MODIM_APP:$MODIM_APP \
    -v $MODIM_HOME:/opt/modim \
    -v $MODIM_APP:/opt/modim_app \
    $IMAGENAME:$VERSION


