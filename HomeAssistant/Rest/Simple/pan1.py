#!/usr/bin/python3

import sqlite3
from dateutil import parser
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


conn = sqlite3.connect("temperature.db")
c=conn.cursor()
c.execute("select timestamp, temperature from house;")
data=c.fetchall()

dates=[]
values=[]
for row in data:
#    dates.append(parser.parse(row[0]))
    dates.append(row[0])
    values.append(row[1])

plt.plot_date(dates,values,'-')
plt.xticks(dates, dates, rotation='vertical')
plt.show()


