#!/usr/bin/env python3

# import haClass 
import sys
from haClass import haClass
from backPorch import backPorch

def main():
    
    ha = backPorch()

    cmdTopic = "/home/outside/PorchLight_1/cmnd/power"


    ha.addTopic('switch.test_start','OFF')

    ha.addTopic('switch.porch_light','OFF')
    ha.changeTopic('switch.porch_light','/home/automation/porch_light')

    ha.Connect()

    ha.dump()
    ha.refresh(1)
    
#    ha.setBooleanValue('switch.test_start')
    
    ha.logic()
    
    ha.run()

    print("Wont get here")


main()
