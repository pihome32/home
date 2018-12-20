#!/usr/bin/env python
# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient
import time
import os


HOST = "localhost"
PORT = 4223
UID = "GKX" # Change XYZ to the UID of your Air Quality Bricklet


dbname = 'home'
user = ''
password = ''
host='localhost'
port=8086

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_air_quality import BrickletAirQuality


loop = 10

def cb_all_values(iaq_index, iaq_index_accuracy, temperature, humidity, air_pressure):
    loop = 10
    # Set period for all values callback to 1s (1000ms)

    if iaq_index_accuracy == BrickletAirQuality.ACCURACY_UNRELIABLE:
        IAQ_accuracy = 0
        IAQ_accuracy_text = "Unreliable"
    elif iaq_index_accuracy == BrickletAirQuality.ACCURACY_LOW:
        IAQ_accuracy = 1
        IAQ_accuracy_text = "Low"
    elif iaq_index_accuracy == BrickletAirQuality.ACCURACY_MEDIUM:
        IAQ_accuracy = 2
        IAQ_accuracy_text = "Medium"
    elif iaq_index_accuracy == BrickletAirQuality.ACCURACY_HIGH:
        IAQ_accuracy = 3
        IAQ_accuracy_text = "High"
    air_quality = "NA"
    if iaq_index < 51:
        air_quality = "Good"
    elif iaq_index < 101 and iaq_index > 50:
        air_quality = "Moderate"
    elif iaq_index < 151 and iaq_index > 100:
        air_quality = "Little bad"	
    elif iaq_index < 201 and iaq_index > 150:
        air_quality = "Unhealthy"
    elif iaq_index < 301 and iaq_index > 200:
        air_quality = "Very unhealthy"
    elif iaq_index > 300 :
        air_quality = "Hazardous"
		
    data_temperature = round((float(temperature)/100),2)
    data_pressure = round(float(air_pressure)/100,1)
    data_humidity=round(float(humidity)/100,2)

	
    client = InfluxDBClient(host, port, user, password, dbname)
    json_body = [
        {
            "measurement": "data",
            "fields": {
                "temperature": data_temperature,
				"humidity": data_humidity,
				"pressure": data_pressure,
				"IAQ_accuracy": IAQ_accuracy,
				"IAQ_accuracy_text": IAQ_accuracy_text,
				"IAQ_index": iaq_index,
				"air_quality": air_quality,
            },
			"tags": {
			"node":"server",
			"location":"salon",
			"sensor":"airquality",
			},
        }
    ]

    client.write_points(json_body)	
	
    ipcon = IPConnection() # Create IP connection
	
	
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    aq = BrickletAirQuality(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register all values callback to function cb_all_values
    aq.register_callback(aq.CALLBACK_ALL_VALUES, cb_all_values)

    # Set period for all values callback to 1s (1000ms)
    aq.set_all_values_callback_configuration(10000, False)
    while loop> 0:
	    
		loop = 10
		

    ipcon.disconnect()