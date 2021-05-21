#!/usr/bin/env python3

# import haClass 
import sys
from haClass import haClass
from backPorch import backPorch

def main():
    
    ha = backPorch()

    ha.loadDefaultIO()    

    if ha.loadIO("../../etc/config.json") == True:     
        print("Failed to load io config")    
    else:    
        print("io config loaded.")    
    

    ha.Connect()
    ha.addTopic('general','TIME','INVALID')
    ha.addTopic('general','SUNRISE','INVALID')
    ha.addTopic('general','SUNSET','INVALID')

    ha.refresh(1)
    
#    ha.setBooleanValue('switch.test_start')
    
    ha.logic()
    
    ha.run()

    print("Wont get here")


main()
