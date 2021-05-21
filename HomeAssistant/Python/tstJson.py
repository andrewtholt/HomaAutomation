#!/usr/bin/env python3

import json


cfgFile = "../../etc/config.json"

with open(cfgFile) as cf:
    cfg = json.load(cf)


print(cfg['MQTT'])

cfg['MQTT']['STATE'] = "ON"

print(cfg['MQTT'])

