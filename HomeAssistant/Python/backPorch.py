
from haClass import haClass

class backPorch(haClass):
    
    cmdTopic = "/home/outside/PorchLight_1/cmnd/power"

    def logic(self):
        print("Back porch light logic")
        
        self.dump()
        
#        start=self.getBooleanValue('switch.test_start')

        state=self.getBooleanValue('switch.porch_light')
        print("State is    ", state)

        self.setBooleanValue( 'switch.porch_light', state )
#        self.setBooleanValue( 'switch.porch_light', start )

        self.dump()
        
#         fans = (start or fans) and (not stop)
#         
#         print("Start is    ", start)
#         print("State       ", state)
#         print("Fans out is ", fans)
#         
#         self.setBooleanValue( 'switch.fans', fans )
