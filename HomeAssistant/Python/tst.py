#!/usr/bin/env python3

import sys 
import os.path
import pymysql as sql 
import json
import paho.mqtt.client as mqtt
import getopt
from requests import get,post

connected=False
# start_topic = "/test/#"
start_topic = set()
data = {}
verbose = True

ip = {}

def restSet(entity_id, state):

    print("restSet")
    print("\t" + entity_id)
    print("\t" + state)
    with open('./haToken.txt', 'r') as content_file:
        tmp = content_file.read()

    token=tmp.strip()

    url = 'http://192.168.10.124:8123/api/services/switch/'
    if stateToLogic(state):
        url += 'turn_on'
    else:
        url += 'turn_off'
    
    headers = { 
        'Authorization': 'Bearer '+ token ,
        'content-type': 'application/json/',
    }

    # payload='{"entity_id": "switch.test"}'
    payload='{"entity_id":"' + entity_id + '"}'

    print(url)
    print(payload)

    r = post(url, data=payload, headers=headers)


def stateToLogic( s ) :

    state = s.upper()

    if state in ["ON","YES","TRUE"]:
        return True

    if state in ["OFF","NO","FALSE"]:
        return False

def logicToState( s ):
    if s:
        return "TRUE"
    else:
        return "FALSE"

def usage():
    print("Usage: logger.py -h| -t <topic> -l <file> -c <cfg file>")

def logic():
    global ip
    global verbose

    print("Logic")

    start = stateToLogic(ip['start'])
    stop = stateToLogic(ip['stop'])
    fans = stateToLogic(ip['switch.fans'])

    print("Start is ", type(start))
    print("Stop  is ",type(stop))
    print("Fans  is ",type(fans))

    fans = (start or fans) and (not stop)

    ip['switch.fans'] = logicToState( fans )

    if verbose:
        print("Start = " , start)
        print("Stop  = " , stop)
        print("Old   = " , logic.old)
        print("Fans  = " , fans)

    if fans != logic.old:
        print("Output to Fans")
        logic.old = fans
        restSet('switch.fans', ip['switch.fans'])
    else:
        print("No change")

logic.old = False

def on_message(client, userData,msg):
    global verbose
    global ip

    print("on_message")

    result = (msg.payload).decode("utf-8")
    print(msg.topic, result);
    print(os.path.basename(msg.topic))
    ip[os.path.basename(msg.topic)] = result

    print(ip)

    logic()


def on_connect(client, userdata, flags, rc):
    global verbose

    print("Connected with result code "+str(rc))
    global connected
    global start_topic

    connected=True
    #
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #
    print(start_topic)
    for topic in start_topic:
        ip[os.path.basename(topic)] = 'OFF'
        client.subscribe(topic)

    print(ip)

def main():
    global verbose
    global start_topic

    verbose=False

    configFile="/etc/mqtt/bridge.json"

    try:
        opts,args = getopt.getopt(sys.argv[1:], "t:vc:h", ["verbose","config=","help"])
        for o,a in opts:
            if o in ["-h","--help"]:
                usage()
                sys.exit()
            elif o in ["-c","--config"]:
                configFile = a
            elif o in ["-v","--verbose"]:
                verbose=True
            elif o in ["-t","--topic"]:
                start_topic.add(a)
                
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    if len(start_topic) == 0:
        print("\nNeed a topic to monitor\n")
        sys.exit(1)

    mqttBroker = 'localhost'
    mqttPort = 1883

    if os.path.exists(configFile):
        with open( configFile, 'r') as f:
            cfg = json.load(f)

        mqttBroker = cfg['local']['name']
        mqttPort   = int(cfg['local']['port'])
    else:
        print(configFile + " not found..")
        print(".. using defaults")

    if verbose:
        print("MQTT Broker : " + mqttBroker)
        print("       Port : " , mqttPort)
        print("      Topic : " , start_topic)


    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message

    mqttClient.connect(mqttBroker, mqttPort, 60)

    global connected
    mqttClient.loop_forever()

main()
