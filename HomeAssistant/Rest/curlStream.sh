#!/bin/bash

set -x

TOKEN=$(cat haToken.txt)

curl -X GET \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    http://192.168.10.124:8123/api/stream
