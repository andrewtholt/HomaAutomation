#!/usr/bin/env python3

# import haClass 
import sys
from haClass import haClass
from fanControl import fanControl

def main():
    
    ha = fanControl()
#    ha = haClass()

    ha.loadDefaultIO()
    if ha.loadIO("../../etc/config.json") == True: 
        print("Failed to load io config")
    else:
        print("io config loaded.")

    ha.dump()

    ha.Connect()

    ha.setBooleanValue('MQTT','start',False)
    ha.setBooleanValue('MQTT','stop',False)
    ha.setBooleanValue('HomeAssistant','fans',False)


#    ha.addTopic('test_start','OFF')
#    ha.addTopic('switch.test_stop','OFF')
#    ha.addTopic('switch.fans','OFF')
    ha.dump()

    ha.refresh(1)
    
#    ha.setBooleanValue('switch.test_start')
    
#    ha.logic()
    
    ha.run()

    print("Wont get here")
    
    for n in range(10):
        ha.refresh(1)
    
        print(ha.getBooleanValue('switch.test_start'))
        
    ha.dump()


main()
