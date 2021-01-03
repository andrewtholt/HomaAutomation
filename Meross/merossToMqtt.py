#!/usr/bin/env python3
import asyncio
import os
import os.path
import json
import getopt
import sys
import signal

from asyncio_mqtt import Client, MqttError

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"

myDevices = {}

config = {}
client =None
verbose=False
plugs = None
runMeross = True

def handler(signum, frame):    
    print('Signal handler called with signal', signum)

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


haveConnected = False
async def simple_example():    
    print("simple_example")
    global client
    global haveConnected


    async with Client("192.168.10.124") as client:    
        if not haveConnected:
            print("I have never connected before")
            print(config)
            for ent in config:
                print(config[ent])
            haveConnected = True

        async with client.filtered_messages("/home/house/#") as messages:    
            await client.subscribe("/home/house/#")
            async for message in messages:    
#                pass
                topic=message.topic
                msg = message.payload.decode()
                print("simple example")
                print(topic)    
                print(msg)

async def mqttMain():    
    # Run the advanced_example indefinitely. Reconnect automatically    
    # if the connection is lost.    

    global client

    print("mqtt main here")
    reconnect_interval = 3  # [seconds]

    print(config['general']['mqtt_server'])
    client = Client(config['general']['mqtt_server'])

    print("Done")

    while True:    
        try:
            print("run simple example")
            await simple_example()    
        except MqttError as error:    
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')    
        finally:
            await asyncio.sleep(reconnect_interval)

async def my_coro(namespace, data, device_internal_id):
    print("I'm here !!!!!!")
    global config
    global plugs
#    print(config['meross'])

    for b in plugs:
        print(b)
        print(f"- {b.name} ({b.type}): {b.online_status} {b.is_on()}")

        if device_internal_id == b.internal_id:
            myName = b.name

    print(data)
    print(namespace)
    print(device_internal_id)

    topic = config['meross'][myName]['mqtt_pub']

    message = ""
    if 'togglex' in data:
        if (data['togglex'][0]['onoff']) == 1:
            print("I'm on")
            message = 'ON'
        else:
            print("I'm off")
            message = 'OFF'
#
    print("Mqtt publish to>" + topic + "<")
    print("Mqtt message   >" + message + "<")

    global client
    print(client)

    await client.publish(topic, message, qos=1)

async def merossMain():
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
        await b.async_update() 
        b.register_push_notification_handler_coroutine(my_coro)

        print(b)
        print(f"- {b.name} ({b.type}): {b.online_status} {b.is_on()}")

    print("\n")
    if len(plugs) < 1:
        print("No devices plugs found...")

    # Close the manager and logout from http_api

    while runMeross:
        await asyncio.sleep(5)

    manager.close()
    manager.stop()
    await http_api_client.async_logout()

# if __name__ == '__main__':
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


    # On Windows + Python 3.8, you should uncomment the following
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    signal.signal(signal.SIGHUP, handler)

    print("i am",os.getpid())

    mainTask = asyncio.ensure_future(merossMain())
    mqttTask = asyncio.ensure_future(mqttMain())

    loop = asyncio.get_event_loop()

    loop.run_forever()

    loop.close()

main()




