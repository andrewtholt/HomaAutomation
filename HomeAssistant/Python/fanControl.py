from haClass import haClass

class fanControl(haClass):
    
    def logic(self):
        print("Fan control logic")
        
        self.dump()
        
        start=self.getBooleanValue('MQTT','start')
        stop =self.getBooleanValue('MQTT','stop')
        fans =self.getBooleanValue('HomeAssistant','fans')
        
        fans = (start or fans) and (not stop)
        
        print("Start is    ", start)
        print("Stop        ", stop)
        print("Fans out is ", fans)
        
        self.setBooleanValue( 'HomeAssistant','fans', fans )
