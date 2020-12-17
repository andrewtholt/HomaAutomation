#!/usr/bin/python3
import json
import sys
import getopt
import os.path

from requests import get,post

def usage():    
    print( "Usage: switch.py -h|--help -j | --json -v|--verbose  -n <name> | --name=<name> -c <cfg file>| --config=<cfg file>")
    print("")        
    print("\t-h|-help\t\tThis.")    
    print("\t-v|--verbose\t\tVerbose.")    
    print("\t-j|--json\t\tOutput in JSON.")    
    print("\t-n <name>|--name=<name>\tName of the device to control.")    
    print("\t-c <cfg>|--config=<cfg>\tLoad this config file.")

def readConfig(fname):    
    if not os.path.isfile(fname):    
        print("Config file " + fname + " does not exist")    
        sys.exit(1)                                                  
                           
    with open(fname) as cf:        
        config = json.load(cf)        
        
        cfg = config["HomeAssistant"]        
    
        return(cfg)


def main():

    configFile = "/etc/HomeAutomation/config.json"
    name = ""
    test = False
    verbose = False
    state = ""
    jssonOut = False

    try:
        opts, args = getopt.getopt( sys.argv[1:], "c:hvn:", ["config=", "help", "name="])
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
        elif o in ("-n", "--name"):
            name = a
        elif o in ("-j","--jason"):
            jsonOut = True

    HARest = readConfig( configFile )

    entity_id = HARest[name]
    if verbose:
        print("Outlet name     :" + name)
        print("Entity ID       :" + entity_id)


    with open('/etc/mqtt/haToken.txt', 'r') as content_file:
        tmp = content_file.read()
    
    token=tmp.strip()

    url = 'http://192.168.10.124:8123/api/states/' + entity_id
    
    headers = {
        'Authorization': 'Bearer '+ token ,
        'content-type': 'application/json/',
    }

#    print(headers);
    
    r = get(url, headers=headers).json()

    print(r['state'])


main()
