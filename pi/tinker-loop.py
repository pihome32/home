#!/usr/bin/env python
# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient


HOST = "localhost"
PORT = 4223
loop = 10

import time

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_master import BrickMaster
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2


UID = "62fTXQ" # Change XXYYZZ to the UID of your Master Brick

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_master import BrickMaster

##Inititalisation
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    master = BrickMaster(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    master.disable_status_led()

    ipcon.disconnect()

UID = "DeD"
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    h = BrickletHumidityV2(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd

    h.set_status_led_config(0)
    ipcon.disconnect()	

#####################################
dbname = 'home'
user = ''
password = ''
host='localhost'
port=8086


# Callback function for humidity callback
def cb_humidity(humidity):
    client = InfluxDBClient(host, port, user, password, dbname)
    json_body = [
        {
            "measurement": "salon",
            "fields": {
                "humidity": round(float(humidity)/100,2),
            }
        }
    ]
    client.write_points(json_body)
    loop = 2
# Callback function for humidity callback
def cb_temperature(temperature):
    client = InfluxDBClient(host, port, user, password, dbname)
    json_body = [
        {
            "measurement": "salon",
            "fields": {
                "temperature": round(float(temperature)/100,2),
            }
        }
    ]
    print('ddfsdsaf')
    loop = 10
    client.write_points(json_body)	
	
def main_loop(loop):
    while loop > 0:
       time.sleep(100)
       loop += 1
	
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    h = BrickletHumidityV2(UID, ipcon) # Create device object
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
    


