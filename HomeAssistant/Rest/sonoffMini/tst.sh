#!/bin/bash

set -x

STATE=$1
curl --libcurl post.c -X POST \
  -H "Content-Type: application/json" \
  -d '{ "deviceid": "1000c8c4b5", "data": { }' \
  http://192.168.10.169:8081/zeroconf/signal_strength
