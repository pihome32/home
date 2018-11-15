#!/usr/bin/env python
# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient
import time
import os


HOST = "localhost"
PORT = 4223
UID = "GKX" # Change XYZ to the UID of your Air Quality Bricklet
lcdUID = "GKb" 

dbname = 'home'
user = ''
password = ''
host='localhost'
port=8086

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_air_quality import BrickletAirQuality
from tinkerforge.bricklet_lcd_128x64 import BrickletLCD128x64


if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    aq = BrickletAirQuality(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    iaq_index, iaq_index_accuracy, temperature, humidity, air_pressure = aq.get_all_values()
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

    if iaq_index < 50:
        air_quality = "good"
    elif iaq_index < 100 and iaq_index > 50:
        air_quality = "average"
    elif iaq_index < 150 and iaq_index > 100:
        air_quality = "little bad"	
    elif iaq_index < 200 and iaq_index > 150:
        air_quality = "bad"
    elif iaq_index < 300 and iaq_index > 200:
        air_quality = "worse"
		
    data_temperature = round((float(temperature)/100),2)
    data_pressure = round(float(air_pressure)/100,1)
    data_humidity=round(float(humidity)/100,2)

	
    ipcon.disconnect()
    client = InfluxDBClient(host, port, user, password, dbname)
    json_body = [
        {
            "measurement": "data",
            "fields": {
                "temperature": data_temperature,
				"humidity": data_humidity,
				"pressure": data_pressure,
				"IAQ_accuracy": IAQ_accuracy,
				"IAQ_index": iaq_index,
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
    lcd = BrickletLCD128x64(lcdUID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
    lcd.set_display_configuration(14,80,0,1)
   #lcd.reset()    # Clear display
    lcd.clear_display()

    # Write "Hello World" starting from upper left corner of the screen
    lcd.write_line(0, 0, "Temperature : " + str(data_temperature))
    lcd.write_line(2, 0, "Humidity : " + str(data_humidity) + "%")
    lcd.write_line(4, 0, "IAQ : " + str(iaq_index) + " / "+ IAQ_accuracy_text)
    lcd.write_line(6, 0, "Air quality : ")
    lcd.write_line(7, 5, air_quality )
	

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
	