#!/usr/bin/python3
import json

from requests import get

import sys

with open('./haToken.txt', 'r') as content_file:
    tmp = content_file.read()

token=tmp.strip()

url = 'http://192.168.10.124:8123/api/states/switch.test'

headers = {
    'Authorization': 'Bearer '+ token ,
    'content-type': 'application/json/',
}

response = get(url, headers=headers)

print(json.dumps(json.loads(response.text), indent=2))
