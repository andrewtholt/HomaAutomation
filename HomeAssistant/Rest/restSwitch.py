#!/usr/bin/python3
import json
import sys
import getopt
import os.path

from requests import get,post

def usage():    
    print( "Usage: switch.py -h|--help -v|--verbose  -n <name> | --name=<name> -c <cfg file>| --config=<cfg file> -o <out|off> | --output=<on|off>")
    print("")    
    print("\t-h|-help\t\tThis.")    
    print("\t-v|--verbose\t\tVerbose.")    
    print("\t-n <name>|--name=<name>\tName of the device to control.")    
    print("\t-c <cfg>|--config=<cfg>\tLoad this config file.")    
    print("\t-o <on|off>|--out=<on|off>\tSet the device to this state.")  

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

    try:
        opts, args = getopt.getopt( sys.argv[1:], "c:ho:vn:t", ["config=", "help", "out=", "name=", "test"])
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
        elif o in ("-o", "--out"):
            state = a
        elif o in ("-n", "--name"):
            name = a
        elif o in ("-t", "--test"):
            test = True
            verbose = True

    HARest = readConfig( configFile )

    entity_id = HARest[name]
    if verbose:
        print("Outlet name     :" + name)
        print("Entity ID       :" + entity_id)
        print("Requested state :" + state)

    with open('/etc/mqtt/haToken.txt', 'r') as content_file:
        tmp = content_file.read()
    
    token=tmp.strip()

#    entity_id = sys.argv[1]
    
    url = 'http://192.168.10.124:8123/api/services/switch/'
    if state == "on":
        url += 'turn_on'
    else:
        url += 'turn_off'
    
    headers = {
        'Authorization': 'Bearer '+ token ,
        'content-type': 'application/json/',
    }
    
    # payload='{"entity_id": "switch.test"}'
    payload='{"entity_id":"' + entity_id + '"}'

    r = post(url, data=payload, headers=headers)
    
    print(r.status_code)

    sys.exit(r.status_code)

main()
