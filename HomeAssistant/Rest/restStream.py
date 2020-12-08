#!/usr/bin/python3
import json

from requests import get

from sseclient import SSEClient
import sys

with open('./haToken.txt', 'r') as content_file:
    tmp = content_file.read()

token=tmp.strip()

url = 'http://192.168.10.124:8123/api/stream'

auth = {
    'Authorization': 'Bearer ' + token 
}

messages = SSEClient(url, headers=auth)

for msg in messages:
    newState = ""

    outputMsg = msg.data
    if type(outputMsg) is str:
        if outputMsg != 'ping':
            outputJS = json.loads(outputMsg.strip())
            print(json.dumps(json.loads(outputMsg), indent=2))

            eventType = outputJS['event_type']
            print(eventType)
            if eventType == 'call_service':
                entityId = outputJS['data']['service_data']['entity_id']
                service = outputJS['data']['service']

#                print(entityId)
#                print(service)

                if service == 'turn_on':
                    newState = 'on'
                elif service == 'turn_off':
                    newState = 'off'

            elif eventType == 'state_changed':
                entityId = outputJS['data']['entity_id']
                newState = outputJS['data']['new_state']['state']

            print(entityId)
            print(newState)


# print(response)
# print(json.dumps(json.loads(response.text), indent=2))
