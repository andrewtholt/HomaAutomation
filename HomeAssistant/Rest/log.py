#!/usr/bin/env python3

import sqlite3 as sqlite
import sys

def main():

    if len(sys.argv) != 2:
        sys.exit(1)

    print(sys.argv[1])
    dbPath = "./log.db"

    con = sqlite.connect(dbPath)
    cur = con.cursor()

    sql = 'insert into ten_minutes (house_temperature) values (' + sys.argv[1] + ');'

    cur.execute( sql )
    con.commit()

    cur.close()




main()
