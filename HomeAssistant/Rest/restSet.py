#!/usr/bin/python3
import json

import sys

from requests import get,post

def main():

    if len(sys.argv) !=3:
        print("Usage:restSet.py <id> <on|off>")
        sys.exit(1)

    with open('/etc/mqtt/haToken.txt', 'r') as content_file:
        tmp = content_file.read()
    
    token=tmp.strip()

    entity_id = sys.argv[1]
    
    url = 'http://192.168.10.124:8123/api/services/switch/'
    if sys.argv[2] == "on":
        url += 'turn_on'
    else:
        url += 'turn_off'
    
    headers = {
        'Authorization': 'Bearer '+ token ,
        'content-type': 'application/json/',
    }
    
    # payload='{"entity_id": "switch.test"}'
    payload='{"entity_id":"' + entity_id + '"}'

    r = post(url, data=payload, headers=headers)
    
    print(r.status_code)

    sys.exit(r.status_code)

main()
