#!/usr/bin/env python3

import asyncio
from contextlib import AsyncExitStack, asynccontextmanager
from random import randrange
from asyncio_mqtt import Client, MqttError

async def simple_example(queue):
    count = 0
    async with Client("192.168.10.124") as client:
        async with client.filtered_messages("/home/house/#") as messages:
            await client.subscribe("/home/house/#")
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
    while True:
        data = await q.get()
        print("Here :",data)

def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(mqttMain(queue))
    asyncio.ensure_future(consumer(queue))

    loop.run_forever()

# asyncio.run(main())
main()

