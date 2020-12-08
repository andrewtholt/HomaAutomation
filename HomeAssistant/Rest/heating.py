#!/usr/bin/python3
import json

import sys
import sqlite3 as sqlite

from requests import get,post

from time import sleep
from datetime import datetime

def main():

    dbPath = "./log.db"

    con = sqlite.connect(dbPath)
    cur = con.cursor()

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
    
    #    print(r)
    #    print(r['state'])
    #    print(r['attributes']['current_temperature'])
        temp=r['attributes']['current_temperature']

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
        print(temp)

        sql = 'insert into ten_minutes (house_temperature) values (' + str(temp) + ');'

        cur.execute( sql )
        con.commit()
        #
        # Sleep for 5 minutes
        #
        sleep(10 * 60)

    cur.close()
main()
