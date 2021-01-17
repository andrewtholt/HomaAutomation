#!/bin/bash 

# set -x

if [  $# -ne 1 ]; then
    echo "Usage $0 <env name>"
    exit 1
fi

# VENV_LOC="$HOME/Virtual/Test"
VENV_LOC="$HOME/Virtual/$1"

VENV_EXISTS=0

if [ -d $VENV_LOC ]; then
    echo "$VENV_LOC exists"
else
    echo "$VENV_LOC does not exist"
    echo "Creating venv ..."
    HERE=$(pwd)

    mkdir -p $VENV_LOC
    cd $VENV_LOC
    cd ..
    mkdir -p $1

    python3.6 -m venv $1
    echo "... done"

    cd $HERE
fi


if [ -f ${VENV_LOC}/pyvenv.cfg ]; then
    echo "pyvenv.cfg exists"
    VENV_EXISTS=1
fi

if [ -d ${VENV_LOC}/Source/Python ]; then
    echo "Source folder exists"
else
    echo "Make Source folder ..."
    mkdir -p ${VENV_LOC}/Source/Python 
    echo "...done"
fi

echo "Copying source ..."
cp *.py ${VENV_LOC}/Source/Python
echo "... done."



