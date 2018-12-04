#!/usr/bin/env python
# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient
import time
import os

# turn on the green LED
os.system("sudo bash -c \"echo 0 > /sys/class/leds/led0/brightness\"")
os.system("sudo bash -c \"echo 0 > /sys/class/leds/led1/brightness\"")

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_master import BrickMaster
from tinkerforge.bricklet_air_quality import BrickletAirQuality


HOST = "localhost"
PORT = 4223

masterUID = "62fTXQ" # Change XXYYZZ to the UID of your Master Brick
humiUID = "DeD"
airUID = "GKX"
lcdUID= "vBK"

##Inititalisation
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    master = BrickMaster(masterUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    master.disable_status_led()

  
    ipcon.disconnect()


if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    air = BrickletAirQuality(airUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    air.set_temperature_offset(2)
    air.set_status_led_config(0)
    ipcon.disconnect()	
	
