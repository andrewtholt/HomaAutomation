#!/usr/bin/env python3
from time import gmtime, strftime
import paho.mqtt.client as mqtt

import pymysql

start_topic = "/home/#"

data = {}

db = None

class database:
    def __init__(self, host, user,password,dbName):
        self.host = host
        self.user = user
        self.password = password
        self.dbName = password
    
        self.db = pymysql.connect( self.host,
                self.user,
                self.password,
                self.dbName )
    
        self.cursor = self.db.cursor()

#    sql = "SELECT VERSION()"
        sql = "select name, state_topic,pointType from mqttQuery where status <> 'DISABLED'"
        self.cursor.execute( sql )

        data = self.cursor.fetchall()

        for n in data:
            print(n[1])

        print("====")

    def getByName(self, name):
        sql = "select name, state_topic,pointType from mqttQuery where name ='" + name + "'"
        self.cursor.execute( sql )

        data = self.cursor.fetchone()

        return data

    def getByTopic(self, topic):
        sql = "select name, state_topic,pointType from,pointType mqttQuery where state_topic ='" + topic + "'"
        self.cursor.execute( sql )

        data = self.cursor.fetchone()

        return data

    def getAllByDeviceType(self, dev_type):
        c = self.db.cursor()

        sql = "select name, state_topic, pointType from mqttQuery where device_type ='" + dev_type + "'"
        sql += " and status = 'ENABLED'"

        print(sql)

        c.execute( sql )

        data = c.fetchall()

        return data

    def updateState(self, topic, state):
        print("Update")
        c = self.db.cursor()

        if state == "ON":
            s = "1"
        else:
            s = "0"

        sql = "update io_point,mqtt set io_point.state = " + s + " where mqtt.name = io_point.name and mqtt.state_topic = '" + topic + "';"
        print(sql)
        c.execute( sql )
        self.db.commit()


def init():
    global data
    global db

    data["START"] = "OFF"

    db = database('192.168.10.124', 'automation','automation','automation')


# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe(start_topic)

    print("Get TASMOTA")

    for node in db.getAllByDeviceType('TASMOTA'):
        print(node[0])
        print(node[1])
        print(node[2])
        client.subscribe( node[1] )
        print("++++")
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global data
    global db
    shortName = ""

    theTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    result = (msg.payload).decode("utf-8")

    if (msg.topic == start_topic):
        shortName = "START"
    # 
    # Update storage here
    # 
    db.updateState( msg.topic, result)
    print(theTime,shortName + " : ",msg.topic, result);
    return


def main():
    init()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

# client.connect("raspberrypi", 1883, 60)
    client.connect("192.168.10.124", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
    client.loop_forever()


main()
