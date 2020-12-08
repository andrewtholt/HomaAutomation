#!/bin/bash

ENTITY="switch.christmas_lights"
TOKEN=$(cat haToken.txt)

curl -s --libcurl post.c -X POST -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.test_start"}' \
  http://192.168.10.124:8123/api/services/switch/turn_off
