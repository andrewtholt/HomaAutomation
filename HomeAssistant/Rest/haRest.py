from requests import get,post
import json

class haRest:

    token=""

    server = "http://192.168.10.124:8123/api/"

    headers=""


    def __init__(self, tokenFile):
#        print("__init__")
        with open('/etc/mqtt/haToken.txt', 'r') as content_file:
            tmp = content_file.read()

        self.token=tmp.strip()

        self.headers = {
            'Authorization': 'Bearer '+ self.token ,
            'content-type': 'application/json/',
        }



    def get(self, entity_id):
#        print("I'm looking for", entity_id)


        url = self.server + "states/" + entity_id

        r = get(url, headers=self.headers).json()

        return r

    def set(self,entity_id, value):
        url = self.server + "services/switch/" 
        v = value.lower()
        if v == "on":    
            print("Switch on")
            url += 'turn_on'    
        else:    
            print("Switch off")
            url += 'turn_off'

        payload='{"entity_id":"' + entity_id + '"}'

        r = post(url, data=payload, headers=self.headers)

        return(r.status_code)


if __name__ == "__main__":
    
    tst = haRest('/etc/mqtt/haToken.txt')
#
#    data = tst.get("sensor.ups_time_left")
#
#    print(data)

    c = tst.set("switch.christmas_lights","off")

    print(c)

