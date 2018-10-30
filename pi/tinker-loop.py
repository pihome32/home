#!/usr/bin/env python
# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient
import time
import os

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_master import BrickMaster
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2

# turn on the green LED
os.system("sudo bash -c \"echo 0 > /sys/class/leds/led0/brightness\"")
os.system("sudo bash -c \"echo 0 > /sys/class/leds/led1/brightness\"")

HOST = "localhost"
PORT = 4223
loop = 10

masterUID = "62fTXQ" # Change XXYYZZ to the UID of your Master Brick
humiUID = "DeD"

dbname = 'home'
user = ''
password = ''
host='localhost'
port=8086

tempComp = -2

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
    h = BrickletHumidityV2(humiUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd

    h.set_status_led_config(0)
    ipcon.disconnect()	

#####################################

humi = 0
# Callback function for humidity callback
def cb_humidity(humidity):
    global humi 
    humi = humidity

# Callback function for humidity callback
def cb_temperature(temperature):
    client = InfluxDBClient(host, port, user, password, dbname)
    json_body = [
        {
            "measurement": "salon",
            "fields": {
                "temperature": round((float(temperature)/100)+tempComp,2),
				"humidity": round(float(humi)/100,2),
            }
        }
    ]
    loop = 1
    client.write_points(json_body)	
	
def main_loop(loop):
    while loop > 0:
       time.sleep(100)
       loop += 1
	
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    h = BrickletHumidityV2(humiUID, ipcon) # Create device object
    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register humidity callback to function cb_humidity
    h.register_callback(h.CALLBACK_HUMIDITY, cb_humidity)
    h.register_callback(h.CALLBACK_TEMPERATURE, cb_temperature)

    # Set period for humidity callback to 1s (1000ms) without a threshold
    h.set_humidity_callback_configuration(10000, False, "x", 0, 0)
    h.set_temperature_callback_configuration(10000, False, "x", 0, 0)
    main_loop(loop)
    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
    


