#!/bin/bash

rm -f temp_graph.png

rrdtool graph temp_graph.png \
-w 785 -h 120 -a PNG \
--slope-mode \
--start -4800 --end now \
--vertical-label "temperature (°C)" \
DEF:temp1=temperatures.rrd:temp1:MAX \
LINE1:temp1#ff0000:"temp 1" 

xdg-open temp_graph.png
