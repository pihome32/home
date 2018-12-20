#!/bin/sh

cd /home/pi/home/pi/
python initial.py
sleep 2
nohup python air.py &
cd /
