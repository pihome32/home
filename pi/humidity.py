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

humiUID = "DeD"


dbname = 'home'
user = ''
password = ''
host='localhost'
port=8086

tempComp = -2

	
#####################################



if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection

    h = BrickletHumidityV2(humiUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    humi = h.get_humidity()
    temperature = h.get_temperature()


    ipcon.disconnect()
    client = InfluxDBClient(host, port, user, password, dbname)
    json_body = [
        {
            "measurement": "data",
            "fields": {
                "temperature": round((float(temperature)/100)+tempComp,2),
				"humidity": round(float(humi)/100,2),
            },
			"tags": {
			"node":"server",
			"location":"salon",
			"sensor":"humidityV2",
			},
        }
    ]

    loop = 1
    client.write_points(json_body)	
    


