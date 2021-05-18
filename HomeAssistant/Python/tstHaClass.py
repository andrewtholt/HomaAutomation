#!/usr/bin/env python3

# import haClass 
import sys
from haClass import haClass
from fanControl import fanControl

def main():
    
    ha = fanControl()
#    ha = haClass()

    if ha.loadIO("../../etc/config.json") == True: 
        print("Failed to load io config")
    else:
        print("io config loaded.")

    sys.exit(1)
    ha.dump()

    ha.Connect()

    ha.addTopic('switch.test_start','OFF')
    ha.addTopic('switch.test_stop','OFF')
    ha.addTopic('switch.fans','OFF')
    ha.dump()
    ha.refresh(1)
    
#    ha.setBooleanValue('switch.test_start')
    
    ha.logic()
    
    ha.run()

    print("Wont get here")
    
    for n in range(10):
        ha.refresh(1)
    
        print(ha.getBooleanValue('switch.test_start'))
        
    ha.dump()


main()
