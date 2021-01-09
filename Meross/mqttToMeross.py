#!/usr/bin/env python3

import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from random import randrange
from asyncio_mqtt import Client, MqttError

import os
import os.path
import sys
import getopt
import json

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager


config = {}
verbose = False
client = None

EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"

def usage():                                   
    print("Usage: merossToMqtt.py -h|--help -v|--verbose -c <cfg file>| --config=<cfg file>")
    print("")
    print("\t-h|-help\t\tThis.")                                     
    print("\t-v|--verbose\t\tVerbose.")                                          
    print("\t-c <cfg>|--config=<cfg>\tLoad this config file.")

def readConfig(fname):
    if not os.path.isfile(fname):
        print("Config file " + fname + " does not exist")
        sys.exit(1)                                   
                                                    
    with open(fname) as cf:                    
        config = json.load(cf)                                        
        
        return(config)    


async def simple_example(queue):
    global client
    count = 0

    async with Client("192.168.10.124") as client:
        async with client.filtered_messages("/home/house/#") as messages:
            for n in config['meross']:
                print("simple_example",config['meross'][n]['mqtt_sub'])
                await client.subscribe(config['meross'][n]['mqtt_sub'])

#            await client.subscribe("/home/house/#")
            async for message in messages:
                print(message.topic)
                print(message.payload.decode())

                count += 1
                print(count)
                await queue.put(message.topic+":" + message.payload.decode())


async def mqttMain(q):
    # Run the advanced_example indefinitely. Reconnect automatically
    # if the connection is lost.
    reconnect_interval = 3  # [seconds]
    while True:
        try:
            await simple_example(q)
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)

async def consumer(q):
    print("Consumer")

    EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"    
    PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"

    # Setup the HTTP client API from user-password    
    # 
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)
    # 
    # Setup and start the device manager    
    # 
    manager = MerossManager(http_client=http_api_client)    
    await manager.async_init()

    await manager.async_device_discovery()


    while True:
        data = await q.get()
        print("Here :",data)
        topic=data.split(":")[0]
        msg  =data.split(":")[1]
        path = topic.split("/") 
        path.pop(0)

        name = path[2]

        print("\tTopic:" + topic)
        print("\tMsg  :" + msg)
        print("\tName :" + name)

        updateTopic = config['meross'][name]['mqtt_pub']
        print("\tTell :" + updateTopic)
        print(client)

        devices = manager.find_devices(device_name=name)
        dev=devices[0]

        print("dev", dev)

        if msg == 'ON':
            await dev.async_turn_on(channel=0)
        elif msg == 'OFF':
            await dev.async_turn_off(channel=0)

        # 
        # TODO: his works but should wait for notification from cloud server.
        # 
        # See ../oldMeross/mqttTest.py line 169
        # 
        await client.publish(updateTopic, msg, qos=1)
#        manager.close()




def main():
    global config
    global verbose 

    try:    
        opts, args = getopt.getopt( sys.argv[1:], "c:hvn:", ["config=", "help","name="])    
    except getopt.GetoptError as err:    
        print(err)    
        usage()    
        sys.exit(2)    
    
    for o, a in opts:    
        if o in ("-v", "--verbose"):    
            verbose = True    
        elif o in ("-c", "--config"):    
            configFile = a               
        elif o in ("-h", "--help"):                              
            usage()    
            sys.exit(0)    
        elif o in ("-n","--name"):    
            name = a    
    
    config = readConfig( configFile)    
    mqttServer = config['general']['mqtt_server']    

    if verbose:     
        print("Config File :" + configFile)    
        print("MQTT Server :" + mqttServer) 

    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(mqttMain(queue))
    asyncio.ensure_future(consumer(queue))
    asyncio.ensure_future(merossMain(queue))

    loop.run_forever()

# asyncio.run(main())
async def merossMain(q):
    global plugs
    print("Meross Main")
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    print("HERE")
    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS210 devices that are registered on this account
    await manager.async_device_discovery()
    plugs = manager.find_devices(device_type="mss210")

    for b in plugs:
        print(b)

main()

