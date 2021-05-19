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
    ioConfigFile = "/etc/HomeAutomation/config.json"

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

    ioCfg = None

    def __logicToState(self, s ) :
        
        if s:
            return 'TRUE'
        else:
            return 'FALSE'
            
    def __stateToLogic(self, s ) :

        state = s.upper()

        if state in ["ON","YES","TRUE"]:
            print("true")
            return True

        if state in ["OFF","NO","FALSE"]:
            print("false")
            return False

    def on_connect(self,client, userdata, flags, rc):
        print("I'm Connected")
        self.connected = True
        
        print("Subscribing to :")
        print(self.subList)
        for t in self.subList:
            print(t)
            topic = self.subList[t]['topic']
            print(topic)
            # 
            # Use REST calls to get current value from Home Assistant.
            # 
            self.mqttClient.subscribe(topic)


    def on_message(self, client, userData,msg):
        print("\nMessage")

        print(self.subList)

        result = (msg.payload).decode("utf-8")

        print(msg.topic, result);
        
        t = os.path.basename(msg.topic)
        print("I am " + t)

        if t in self.subList:
            print("Found")
        else:
            print("Not Found")

            for n in self.subList:
                fred = self.subList[n]['topic']

                if self.subList[n]['topic'] == msg.topic:
                    print("Topic found",n)
                    t = n
                    break

        self.subList[ t ]['state'] = self.__stateToLogic(result)

        print("======================++")
        
        self.logic()

    def loadDefaultIO(self):
        print("Loading default ioConfig from:"+ self.ioConfigFile )
        fail = True
        if os.path.exists(self.ioConfigFile):
            with open( ioConfigFile, 'r') as f:
                self.ioCfg = json.load(f)
                print(self.ioCfg)
            fail =False
        else:
            print(self.ioConfigFile + " not found")
            fail = True
        return fail


    def loadIO(self, ioFile):
        print("Loading ioConfig from:"+ ioFile )
        if os.path.exists(ioFile):
            print("File Exists")
            with open( ioFile, 'r') as f:
                self.ioCfg = json.load(f)
                print(self.ioCfg['MQTT'])
        else:
            print(self.ioConfigFile + " not found..")
            sys.exit(1)

    def __init__(self):
        if os.path.exists(self.configFile):
            print("Loading Config file:" + self.configFile)
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
        
    def changeTopic(self, name, topic):
        self.subList[name]['topic'] = topic
        if self.connected:
            self.mqttClient.subscribe(topic)

    def addTopic(self, t, default):
        print("addTopic")
        self.subList[t] = {'topic':'', 'state':self.__stateToLogic(default) }
        
        topic = self.baseTopic + t
        print("\t"+topic)

        self.subList[t]['topic'] = topic

        print("\t" + topic)
        if self.connected:
            print("Subscribe.")
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
       print("===")
       print(self.subList)
       print("===")
       for name in self.subList:
#           print("\t" + topic + "=" + self.subList[name]['topic'])
           print("\t" + name + "=" , self.subList[name])
           
    # 
    # Lookup the value and return a boolean 
    # 
    def getBooleanValue(self, name):
        print(name)
        print( self.subList[ name ]['state'])
#        return self.__stateToLogic( self.subList[ name ]['state'])
        return self.subList[ name ]['state']

    def setBooleanValue(self, name, state):
#        print(self.url)
        
        url=self.url  
        
        if state:
#        if self.getBooleanValue(name):
            url += 'turn_on'
            self.subList[name]['state'] = True
        else:
            url += 'turn_off'
            self.subList[name]['state'] = False
        
        headers = {
            'Authorization': 'Bearer '+ self.token ,
            'content-type': 'application/json/',
        }
        
        # payload='{"entity_id": "switch.test"}'
        payload='{"entity_id":"' + name + '"}'
    
        print(headers)
        print(url)
        print(payload)
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



