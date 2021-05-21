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
    
    ioCfg = None

    def readConfig(self,fname):        
        cfg = None

        if not os.path.isfile(fname):        
            print("Config file " + fname + " does not exist")        
            sys.exit(1)                                                      
                               
    # TODO catch exception, or test file existence
        with open(fname) as cf:            
            cfg = json.load(cf)            
            
#            cfg = config["HomeAssistant"]            
        
        return(cfg)

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
        
#        self.findJson('fans','',all_paths)

        print("Subscribing to :")
        for t in self.ioCfg['MQTT']:
            print("name",t)
            topic = self.ioCfg['MQTT'][t]['mqtt_sub']
            print("Topic " + self.ioCfg['MQTT'][t]['mqtt_sub'])
            print("xxxxxxxxxx")
            print("------")
            # 
            # Use REST calls to get current value from Home Assistant.
            # 
            self.mqttClient.subscribe(topic)


    def findIO(self, name):

        result = []

        for f in self.ioCfg:
            if name in self.ioCfg[f]:
                print("->Found " + name + " in " + f)
                result.append(f)
                result.append(name)

        return result


    def on_message(self, client, userData,msg):
        print("\nMessage")

        result = (msg.payload).decode("utf-8")

        print(msg.topic, result);
        
        t = os.path.basename(msg.topic)
        print("I am " + t)
        print("\t" + result)

        place=self.findIO( t )

        print("len", len(place))
        base=place[0]
        print("base", base)
        item=place[1]
        print("item", item)

        if t in self.ioCfg[base]:
            print("Found")
        else:
            print("Not Found")

            for n in self.ioCfg:
                fred = self.ioCfg[n]['topic']

                if self.ioCfg[n]['topic'] == msg.topic:
                    print("Topic found",n)
                    t = n
                    break
                else:
                    print("Still not found")

        print("HERE /////////////////++")
        print("A")
        print("and")

        print((self.ioCfg[base][ item ]['state']) is bool)

        if type(self.ioCfg[base][ item ]['state']) is bool:
            print("BOOL")
            self.ioCfg[base][ item ]['state'] = self.__stateToLogic(result)
        else:
            print("STRING")
            self.ioCfg[base][ item ]['state'] = result

        print("======================++")
        
        self.logic()

    def loadDefaultIO(self):
        print("Loading default ioConfig from:"+ self.ioConfigFile )
        fail = True
        if os.path.exists(self.ioConfigFile):
            self.ioCfg = self.readConfig( self.ioConfigFile)

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
            self.ioCfg = self.readConfig( ioFile)

            print(self.ioCfg['MQTT'])
        else:
            print(self.ioConfigFile + " not found..")
            sys.exit(1)

    def __init__(self):
        if os.path.exists(self.configFile):
            print("Loading Config file:" + self.configFile)

            cfg = self.readConfig( self.configFile )
#            with open( self.configFile, 'r') as f:
#                cfg = json.load(f)

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

    def addTopic(self,section, name, default):
        print("addTopic")

#        self.subList[t] = {'topic':'', 'state':self.__stateToLogic(default) }


        print(section, name)
        print(self.ioCfg[section][name])

        if self.ioCfg[section][name]['state'] is bool:
            self.ioCfg[section][name]['state'] = self.__stateToLogic(default)
        else:
            self.ioCfg[section][name]['state'] = default

        topic = self.ioCfg[section][name]['mqtt_sub']

        print("\t" + topic)
        if self.connected:
            print("Subscribe:" + topic )
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
       
       for section in self.ioCfg:
           print("Section : " +section)
           for item in self.ioCfg[section]:
               print("\tItem    : " +item)
               print("\t" , self.ioCfg[section][item])

    def getValue(self, section, name):
#        print("GET VALUE")
#        print(section,name)
#        print(self.ioCfg[section][ name ])

        if 'state' in self.ioCfg[section][ name ]:
            print("Found")
        else:
            print("Not Found")
            self.ioCfg[section][ name ]['state'] = ''

        return self.ioCfg[section][ name ]['state']
    # 
    # Lookup the value and return a boolean 
    # 
    def getBooleanValue(self, section, name):
        print(name)

        if 'state' in self.ioCfg[section][ name ]:
            pass
#            print("Found")
        else:
            print("Not Found")
            self.ioCfg[section][ name ]['state'] = False

        print( self.ioCfg[section][ name ]['state'])
        print("+++++")
#        return self.__stateToLogic( self.subList[ name ]['state'])
        return self.ioCfg[section][ name ]['state']


    def setValue(self, section, name, state):
        url=self.url  
        
        print(self.ioCfg[section])
        self.ioCfg[section][ name ]['state'] = state

        

    def setBooleanValue(self, section, name, state):
        
        url=self.url  
        
#        print(self.ioCfg[section])
        if state:
#        if self.getBooleanValue(name):
            url += 'turn_on'
            self.ioCfg[section][name]['state'] = True
        else:
            url += 'turn_off'
            self.ioCfg[section][name]['state'] = False
        
        headers = {
            'Authorization': 'Bearer '+ self.token ,
            'content-type': 'application/json/',
        }
        
        # payload='{"entity_id": "switch.test"}'
        if section == 'HomeAssistant':
            payload='{"entity_id":"' + self.ioCfg[section][name]['name'] + '"}'
        else:
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



