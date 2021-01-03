#!/usr/bin/env python3
import asyncio
import os
import sys
import getopt 
import json

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager


EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"

def usage():
    print("Usage: info.py -h|--help -v|--verbose -n <name> | --name=<name> -c <cfg file>| --config=<cfg file>")
    print("")    
    print("\t-h|-help\t\tThis.")
    print("\t-v|--verbose\t\tVerbose.")
    print("\t-c <cfg>|--config=<cfg>\tLoad this config file.")
    print("\t-name <name>|--name=<name>\tPlug name.")

    
def readConfig(fname):    
    if not os.path.isfile(fname):
        print("Config file " + fname + " does not exist")
        sys.exit(1)
    
    with open(fname) as cf:        
        config = json.load(cf)        
        
#        sonoff = config["SonoffDIY"]        
    
        return(config)    


async def merossMain(name):

    print(name)
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS210 devices that are registered on this account
    await manager.async_device_discovery()

    fred = manager.find_devices(device_name=name)

#    print("fred", fred)

    dev = fred[0]

    await dev.async_update()

    if dev.is_on():
        print(name + " is ON")
    else:
        print(name + " is OFF")

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

def main():

    configFile = "/etc/HomeAutomation/config.json"        
    name = ""         

    verbose = False

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


    if verbose:
        print("Name        :" + name)
        print("Config File :" + configFile)

    getState = readConfig( configFile)

    print(getState)
    # On Windows + Python 3.8, you should uncomment the following
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(merossMain(name))
    loop.close()


main()
