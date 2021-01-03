#!/bin/bash

set -x

echo "Creating db ..."
mysql -h 192.168.10.124 -u automation -pautomation < ./mysqlNewSetup.sql

if [  $? -ne 0 ]; then
    echo"Create db failed"
    exit 1
else
    echo "... done"
fi

echo "Loading db ..."
mysql -D automation -h 192.168.10.124 -u automation -pautomation < ./tst.sql

if [  $? -ne 0 ]; then
    echo"Load db failed"
    exit 1
else
    echo "... done"
fi

