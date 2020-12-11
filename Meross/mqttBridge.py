#!/usr/bin/env python3
import asyncio
import os
import os.path
import json

from asyncio_mqtt import Client, MqttError

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"

myDevices = {}

config = {}
client =None

async def simple_example():    
    print("simple_example")
    global client
    async with Client("192.168.10.124") as client:    
        async with client.filtered_messages("/home/house/#") as messages:    
            await client.subscribe("/home/house/#")
            async for message in messages:    
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
#    client = Client("192.168.10.124")
#    client = Client("test.mosquitt.org")
#    await stack.enter_async_context(client)
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
    print(config)

    print(data)
    print(namespace)
    print(device_internal_id)

    myName = myDevices[device_internal_id]

    print("My name is ", myName)

    topic = config[myName]['mqtt_pub']

    message = ""
    if 'togglex' in data:
        if (data['togglex'][0]['onoff']) == 1:
            print("I'm on")
            message = 'on'
        else:
            print("I'm off")
            message = 'off'

    print("Mqtt publish to>" + topic + "<")
    print("Mqtt message   >" + message + "<")
    global client
    await client.publish(topic, message, qos=1)
#    await asyncio.sleep(2)
    print("========================================")

async def main():
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS210 devices that are registered on this account
    await manager.async_device_discovery()
#    plugs = manager.find_devices(device_type="mss210")

    fred = manager.find_devices(device_name="conservatory")

    print("fred", fred[0])

    dev = fred[0]
    print(dev.internal_id)

    myDevices[dev.internal_id] = "conservatory"

    await dev.async_update()
    print("fred is ", dev.is_on())

    dev.register_push_notification_handler_coroutine(my_coro)

#    await dev.async_turn_on(channel=0)

    print(f"fred is {dev.name} ({dev.type}): {dev.online_status} {dev.is_on()}")


#    all_devices = manager.find_devices()
    plugs = manager.find_devices()

    for b in plugs:
        print(b)
        print(f"- {b.name} ({b.type}): {b.online_status}")

    print("\n")
    if len(plugs) < 1:
        print("No devices plugs found...")

    # Close the manager and logout from http_api

    while True:
        await asyncio.sleep(50)

    manager.close()
    await http_api_client.async_logout()

if __name__ == '__main__':

    config_file = open('config.json')

    config = json.load(config_file)

    print(config)

    # On Windows + Python 3.8, you should uncomment the following
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    mainTask = asyncio.ensure_future(main())
    mqttTask = asyncio.ensure_future(mqttMain())

    loop = asyncio.get_event_loop()

    loop.run_forever()

#    loop.run_until_complete(main())

    loop.close()





