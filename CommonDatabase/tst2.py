#!/usr/bin/python3

import yaml

with open("/home/andrewh/Data/HomeAssistant/c1.yaml", 'r') as f:

    doc = yaml.safe_load(f)
# To access branch1 text you would use:

    print("===== sensor")
    txt = doc["sensor"]

    for n in txt:
        try:
            print(n['name'])
        except:
            pass

    print("===== binary sensor")
    txt = doc["binary_sensor"]

    for n in txt:
        try:
            print(n['name'])
        except:
            pass

    print("===== switch")
    txt = doc["switch"]

    for n in txt:
        try:
            if(n['platform']) == 'mqtt':
                name = ('switch.' + n['name'].replace(" ","_")).lower()
                print("Name     :" +  name)

                print('Cmd topic:' + n['command_topic'])
                print('=========')
        except:
            print('--> error')
