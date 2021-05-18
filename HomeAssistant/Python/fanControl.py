from haClass import haClass

class fanControl(haClass):
    
    def logic(self):
        print("Fan control logic")
        
        self.dump()
        
        start=self.getBooleanValue('switch.test_start')
        stop =self.getBooleanValue('switch.test_stop')
        fans =self.getBooleanValue('switch.fans')
        
        fans = (start or fans) and (not stop)
        
        print("Start is    ", start)
        print("Stop        ", stop)
        print("Fans out is ", fans)
        
        self.setBooleanValue( 'switch.fans', fans )
