#!/bin/bash

rrdtool create temperatures.rrd \
--step 300 \
DS:temp1:GAUGE:600:0:50 \
RRA:MAX:0.5:1:288 \
RRA:MIN:0.5:12:288 \
RRA:AVERAGE:0.5:12:288

