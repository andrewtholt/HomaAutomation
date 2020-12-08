#!/usr/bin/python3
import json

import sys

from requests import get,post

def main():

    if len(sys.argv) !=2:
        print("Usage:")
        sys.exit(1)

    with open('/etc/mqtt/haToken.txt', 'r') as content_file:
        tmp = content_file.read()
    
    token=tmp.strip()

    entity_id = sys.argv[1] 
#   GET /api/states/<entity_id> 
    url = 'http://192.168.10.124:8123/api/states/' + entity_id
    
    headers = {
        'Authorization': 'Bearer '+ token ,
        'content-type': 'application/json/',
    }

    print(headers);
    
    r = get(url, headers=headers).json()

    print(r['state'])


main()
