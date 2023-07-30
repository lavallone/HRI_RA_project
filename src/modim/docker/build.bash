#!/bin/bash

IMAGENAME=modim

VERSION=1.0.1

DOCKERFILE=Dockerfile

docker build -t $IMAGENAME:$VERSION -f $DOCKERFILE .

docker tag $IMAGENAME:$VERSION $IMAGENAME:latest
docker tag $IMAGENAME:$VERSION iocchi/$IMAGENAME:latest

