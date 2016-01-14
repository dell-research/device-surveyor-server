#!/bin/bash

PROG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $PROG_DIR

ip addr show
python2 com/dell/research/devicesurveyorserver/surveyorserver.py

popd
