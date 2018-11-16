#!/usr/bin/env python
# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient
import time
import os

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2


HOST = "localhost"
PORT = 4223
loop = 10

UID = "DeD"


dbname = 'home'
user = ''
password = ''
host='localhost'
port=8086

tempComp = -2



#####################################
def cb_temperature(temperature):
    global data_temperature
    data_temperature=temperature

def cb_humidity(humidity):
    client = InfluxDBClient(host, port, user, password, dbname)
    json_body = [
        {
            "measurement": "data",
            "fields": {
				"humidity": round((float(humidity)/100),2),
				"temperature": round((float(data_temperature)/100),2),
			},
			"tags": {
			"node":"server",
			"location":"salon",
			"sensor":"humidityV2",
			},
        }
    ]
    print(data_temperature)

    client.write_points(json_body)	

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    h = BrickletHumidityV2(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register humidity callback to function cb_humidity
    
    h.register_callback(h.CALLBACK_TEMPERATURE, cb_temperature)
    h.register_callback(h.CALLBACK_HUMIDITY, cb_humidity)

    # Set period for humidity callback to 1s (1000ms) without a threshold
    h.set_temperature_callback_configuration(1000, False, "x", 0, 0)
    h.set_humidity_callback_configuration(1000, False, "x", 0, 0)
    while True:
	    loop += 1
    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
