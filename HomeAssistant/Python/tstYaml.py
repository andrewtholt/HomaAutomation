#!/usr/bin/env python3

import yaml
from sys import exit

# myConfig=""
with open("example.yaml", 'r') as stream:
    try:
#        print(yaml.safe_load(stream))
        myConfig=yaml.safe_load(stream)
#        print(myConfig)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

for n in myConfig['automation']:

    service=n['action']['service']
    if service == 'mqtt.publish':
        print("Service  : "+service)
        print("entity_id: "+ n['trigger']['entity_id'])
        topic=n['action']['data_template']['topic']
        print("topic    :"+ topic)
        print("====")


exit(0)

print('====== switch =========' )
for n in myConfig['switch']:
    if n['platform'] == 'mqtt':
        tst=n['name']
        topic=n['state_topic']

        name=(".".join(tst.split())).lower()
        print(name)
        print(topic)
        print('======')

print('====== binary_sensor =========' )
for n in myConfig['binary_sensor']:
    if n['platform'] == 'mqtt':
        tst=n['name']
        topic=n['state_topic']

        name=(".".join(tst.split())).lower()
        print(name)
        print(topic)
        print('======')

