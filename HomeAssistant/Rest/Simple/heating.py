#!/usr/bin/python3
import json

import sys
import sqlite3 as sqlite

from requests import get,post

from time import sleep, time
from datetime import datetime

def align():
    Slice = 600 # 10 minutes
    now=int(time())

    f = now % Slice

    delay = Slice - f

    hms = datetime.now()
    dt_string = hms.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    print("Sleep for ", delay)

    sleep(delay)

def main():

    firstTime = True
    dbPath = "./temperature.db"

    con = sqlite.connect(dbPath)
    cur = con.cursor()
    
    # wait until the minutes past the hour is a multiple of 10

    

    while True:
        with open('./haToken.txt', 'r') as content_file:
            tmp = content_file.read()
        
        token=tmp.strip()
    
        entity_id = 'climate.heating'
    
    #   GET /api/states/<entity_id> 
        url = 'http://192.168.10.124:8123/api/states/' + entity_id
        
        headers = {
            'Authorization': 'Bearer '+ token ,
            'content-type': 'application/json/',
        }
        
        r = get(url, headers=headers).json()
    
        temp=r['attributes']['current_temperature']

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
        print(temp)

        sql = 'insert into house (temperature) values (' + str(temp) + ');'

        cur.execute( sql )
        con.commit()
        #
        # Sleep for 10 minutes
        #
        if firstTime:
            align()
            firstTime = False
        else:
            sleep(10 * 60)

    cur.close()
main()
