#!/bin/bash 

# set -x

VERBOSE="NO"
NAME=""

PYTHON="python3"
BASE_DIR="${HOME}/MyVirtual"

while getopts ":hn:p:v" opt; do
    case ${opt} in
        v )
            VERBOSE="YES"
            ;;
        h )
            echo "Help"
            ;;
        n )
            NAME=$OPTARG
            ;;
        p )
            PYTHON_VER=$OPTARG
            PYTHON="python${PYTHON_VER}"
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            ;;
        : )
            echo "Invalid option: $OPTARG requires an argument" 1>&2
            ;;
    esac
done

VENV_LOC=${BASE_DIR}/${NAME}
echo

if [ $VERBOSE = "YES" ]; then
    echo
    echo "Name   : $NAME"
    echo "Python : $PYTHON"
    echo "Base   : $BASE_DIR"
    echo "Venv   : $VENV_LOC"
fi

if [ -d $BASE_DIR ]; then
    echo "Base folder $BASE_DIR exists"
else
    echo "Base folder $BASE_DIR does not exist"
    echo "Making ..."
    echo "... done."
fi

if [ -d ${VENV_LOC} ]; then
    echo "ERROR: venv folder ${VENV_LOC} exists, exiting"
    exit 1
fi

shift $((OPTIND -1))

HERE=$(pwd)

mkdir -p $VENV_LOC
cd $VENV_LOC
cd ..

echo "Creating venv."
$PYTHON -m venv $NAME
echo "... done"

cd $HERE

if [ -f ${VENV_LOC}/pyvenv.cfg ]; then
    echo "Sucess: pyvenv.cfg exists"
    VENV_EXISTS=1
else
    echo "ERROR: Failed to create venv."
    exit 2
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



