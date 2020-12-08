#!/usr/bin/env python3

import sys 
import os.path
import pymysql as sql 
import json
import paho.mqtt.client as mqtt
import getopt
import time
from requests import get,post

connected = False
    
class haClass(object):
    configFile="/etc/mqtt/bridge.json"
    mqttBroker = '127.0.0.1'
    mqttPort = 1883
    verbose = True
    connected=False
    mqttClient=None
    url = 'http://127.0.0.1:8123/api/services/switch/'
    
    homeAssistant='127.0.0.1'
    homeAssistantPort = 8123
    token=""
    
    baseTopic = '/home/homeAssistant/'
    
    subList = {}

    def __logicToState(self, s ) :
        
        if s:
            return 'TRUE'
        else:
            return 'FALSE'
            
    def __stateToLogic(self, s ) :

        state = s.upper()

        if state in ["ON","YES","TRUE"]:
            return True

        if state in ["OFF","NO","FALSE"]:
            return False

    def on_connect(self,client, userdata, flags, rc):
        print("I'm Connected")
        self.connected = True
        
        print("Subscribing to :")
        for t in self.subList:
            # 
            # Use REST calls to get current value from Home Assistant.
            # 
            topic = self.baseTopic + t
            print("\t" + topic)
            self.mqttClient.subscribe(topic)


    def on_message(self, client, userData,msg):
        print("Message")
        result = (msg.payload).decode("utf-8")
        print(msg.topic, result);
        
        t = os.path.basename(msg.topic)
        self.subList[ t ] = result
        print("======================++")
        
        self.logic()

    def __init__(self):
        if os.path.exists(self.configFile):
            print("Loading file")
            with open( self.configFile, 'r') as f:
                cfg = json.load(f)

            self.mqttBroker = cfg['local']['name']
            self.mqttPort   = int(cfg['local']['port'])
            
            self.homeAssistant = cfg['home_assistant']['name']

            self.homeAssistantPort = cfg['home_assistant']['port']
            
            self.url = 'http://' + self.homeAssistant + ":" + self.homeAssistantPort + '/api/services/switch/'

        else:
            print(configFile + " not found..")
            print(".. using defaults")
            
        with open('./haToken.txt', 'r') as content_file:
            tmp = content_file.read()
            
        self.token=tmp.strip()
            
        
    def Connect(self):
        
        self.mqttClient = mqtt.Client()
        self.mqttClient.connect(self.mqttBroker, self.mqttPort, 60)
        
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = self.on_message
       
        while not self.connected:
            print("Waiting ...")
            self.mqttClient.loop()
            time.sleep(0.1)
        
    def addTopic(self, t, default):
        self.subList[t] = default
        
        if self.connected:
            print("Subscribe.")
            topic = self.baseTopic + t
            print("\t" + topic)
            self.mqttClient.subscribe(topic)
            
    def refresh(self):
        print("Loop")
        self.mqttClient.loop()
        
    def refresh(self, loops):
        for n in range(loops):
            self.mqttClient.loop()
            time.sleep(0.1)
            
    def run(self):
        self.mqttClient.loop_forever()
        
    def dump(self):
       print("Config File   :" + self.configFile)
       print("MQTT Broker   :" + self.mqttBroker)
       print("MQTT Port     :" , self.mqttPort)
       print("")
       print("Home Assistant:" , self.homeAssistant)
       print("     Ports    :" , self.homeAssistantPort)
       print("     URL      :" , self.url)
       
       print("     Token    :" + self.token)
       
       print("Sub list")
       for topic in self.subList:
           print("\t" + topic + "=" + self.subList[topic])
           
    # 
    # Lookup the value and return a boolean 
    # 
    def getBooleanValue(self, name):
        print(name)
        print( self.subList[ name ])
        return self.__stateToLogic( self.subList[ name ])

    def setBooleanValue(self, name, state):
#        print(self.url)
        
        url=self.url  
        
        if state:
#        if self.getBooleanValue(name):
            url += 'turn_on'
            self.subList[name] = 'ON'
        else:
            url += 'turn_off'
            self.subList[name] = 'OFF'
        
        headers = {
            'Authorization': 'Bearer '+ self.token ,
            'content-type': 'application/json/',
        }
        
        # payload='{"entity_id": "switch.test"}'
        payload='{"entity_id":"' + name + '"}'
    
#        print(headers)
#        print(url)
#        print(payload)
        r = post(url, data=payload, headers=headers)
        
    
    def logic(self):
        # override this
        print("Base class, override me")
    
if __name__ == "__main__":
    # execute only if run as a script
    print("Executing")
    ha = haClass()
    
    ha.addTopic('switch.fans','OFF')
    ha.Connect()
    ha.dump()
    ha.refresh(1)
    
    ha.setBooleanValue('switch.fans')
    
    sys.exit(0)
    
    for n in range(10):
        ha.refresh(1)
    
        print(ha.getBooleanValue('switch.fans'))
        
    ha.dump()



