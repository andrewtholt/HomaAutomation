#!/usr/bin/env python3
import asyncio
import os
import sys

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"


async def main(name, state):

    print(name,state)
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS210 devices that are registered on this account
    await manager.async_device_discovery()

    fred = manager.find_devices(device_name="conservatory")

    print("fred", fred[0])

    dev = fred[0]

    await dev.async_update()

    if state == "on":
        await dev.async_turn_on(channel=0)
    else:
        await dev.async_turn_off(channel=0)

    if dev.is_on():
        print("fred is ON")
    else:
        print("fred is OFF")

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print("Usage: switch.py <name> <on|off>")
        sys.exit(1)

    name = sys.argv[1]
    state = sys.argv[2]
    # On Windows + Python 3.8, you should uncomment the following
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(name,state))
    loop.close()
