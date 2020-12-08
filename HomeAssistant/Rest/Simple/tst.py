#!/usr/bin/python3

from time import time, sleep
from datetime import datetime


hms = datetime.now()
dt_string = hms.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)
now=int(time())

f = now% 600

print("f=",f)
print(600-f)

sleep(600-f)

hms = datetime.now()
dt_string = hms.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

