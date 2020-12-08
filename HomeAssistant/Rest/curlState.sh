#!/bin/bash

# set -x

TOKEN=$(cat haToken.txt)

curl --libcurl getCode.c -X GET \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    http://192.168.10.124:8123/api/states/switch.test_start
