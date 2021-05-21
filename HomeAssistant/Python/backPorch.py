
from haClass import haClass


class backPorch(haClass):
    
    def timeToMinutes(self, timeString):
        tmp = timeString.split(':')

        out = (int(tmp[0]) *60) + int(tmp[1])

        return out


    def logic(self):
        print("Back porch light logic")
        
        state=self.getBooleanValue('MQTT','start')

        time = self.getValue("general","TIME")
        sunrise = self.getValue("general","SUNRISE")
        sunset  = self.getValue("general","SUNSET")


        self.setBooleanValue('HomeAssistant', 'porch_light', state )
        light = self.getBooleanValue('HomeAssistant','porch_light')

        print("TIME",time)
        print("SUNRISE",sunrise)
        print("SUNSET ",sunset)
        print("Start is    ", state)

        if time != "INVALID":

            morningOn  = self.timeToMinutes("05:30")
            morningOff = self.timeToMinutes(sunrise) + 30
            sr = self.timeToMinutes(sunrise)

            eveningOn = self.timeToMinutes(sunset) - 30
            eveningOff= self.timeToMinutes("23:00")
            ss = self.timeToMinutes(sunset)

            now = self.timeToMinutes(time)

            output = False

            print("Start ============================")
            print("now    ", now )

            print("morningOn ", morningOn)
            print("Sunrise   ", sr)
            print("morningOff", morningOff)

            print("eveningOn", eveningOn)
            print("Sunset   ", ss)
            print("eveningOff", eveningOff)
            print("")

            if morningOn <= sr and morningOff >= sr:
                print("Morning")
                if morningOn <= now and morningOff >= now:
                    print("ON")
                    output = True
                else:
                    print("OFF")
                    output = False

            if eveningOn <= ss and eveningOff >= ss:
                print("Evening")

                if eveningOn <= now and eveningOff >= now:
                    print("ON")
                    output = True
                else:
                    print("OFF")
                    output = False

            print("output",output)                
            print("End ==============================")


            self.setBooleanValue('HomeAssistant', 'porch_light', state )

            light = self.getBooleanValue('HomeAssistant','porch_light')
        print("Light is    ", light)
        
#         fans = (start or fans) and (not stop)
#         
#         print("Start is    ", start)
#         print("State       ", state)
#         print("Fans out is ", fans)
#         
#         self.setBooleanValue( 'switch.fans', fans )
