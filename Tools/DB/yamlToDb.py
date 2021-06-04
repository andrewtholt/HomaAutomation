#!/usr/bin/env python3

import yaml
import sqlite3
from sys import exit

# myConfig=""

connection = sqlite3.connect("HA.db")
crsr = connection.cursor()

with open("configuration.yaml", 'r') as stream:
    try:
        myConfig=yaml.safe_load(stream)
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


print('====== switch =========' )
sql = ""

for n in myConfig['switch']:

    sql = 'insert or replace into HA (entity_id, data_type,'
    if n['platform'] == 'snmp':
        tst=n['name']

        if ' ' in tst:
            name=(".".join(tst.split())).lower()
        else:
            name = "switch." + tst.lower()

        print("entity_id  :" + name)
        out = sql + ' cmd_topic,state_topic) values ("%s","%s","%s","%s");'%(name,'switch','', '')
        print(out)
        crsr.execute( out )
        connection.commit()

    if n['platform'] == 'mqtt':
        tst=n['name']
        cmd_topic=n['command_topic']
        state_topic=n['state_topic']

        name=(".".join(tst.split())).lower()
        print("entity_id  :" + name)
        print("State Topic:" + state_topic)
        print("Cmd Topic  :" + cmd_topic)

        out = sql + ' cmd_topic,state_topic) values ("%s", "%s","%s","%s");'%(name,"switch",cmd_topic, state_topic)
        print(out)
        crsr.execute( out )
        connection.commit()
        print('======')

print('====== binary_sensor =========' )
for n in myConfig['binary_sensor']:
    if n['platform'] == 'mqtt':
        tst=n['name']
        topic=n['state_topic']

        print(tst)
        name=(".".join(tst.split())).lower()
        print(name)
        print(topic)
        out = sql + ' cmd_topic,state_topic) values ("%s", "%s","%s","%s");'%(name,"binary_sensor",cmd_topic, state_topic)
        print(out)
        crsr.execute( out )
        connection.commit()
        print('======')
connection.close()

