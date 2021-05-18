#!/usr/bin/env python3

import datetime

now = datetime.datetime.now()
t = now.time()

hNow = t.hour
mNow = t.minute

tNow = (t.hour*60) + mNow

onAt = ( 5 * 60) + 44

sunrise = ( 5 * 60) + 3

offAt=sunrise + 30

print("onAtt", onAt)
print("sunrise", sunrise)
print("offAt",offAt)

if onAt < sunrise and offAt > sunrise:
    if onAt < tNow and offAt > tNow:
        print(">ON")
    else:
        print(">OFF")
else:
    print("Do Nothing")


