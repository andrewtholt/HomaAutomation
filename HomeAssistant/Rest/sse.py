#!/usr/bin/python3 

from sseclient import SSEClient
import json
import sys
from requests import get,post

with open('./haToken.txt', 'r') as content_file:
    tmp = content_file.read()

token=tmp.strip()


# auth = {'Authorization': 'Bearer ABCDEFGH'}
auth = {'Authorization': 'Bearer ' + token }
messages = SSEClient('http://192.168.10.124:8123/api/stream', headers=auth)

for msg in messages:
#    print(msg)
    outputMsg = msg.data

    print(type(outputMsg))

    if type(outputMsg) is str:
#        print(">" + outputMsg + "<")

        if outputMsg != 'ping':
            print(json.dumps(json.loads(outputMsg), indent=2))
