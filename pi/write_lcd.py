#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import paho.mqtt.client as mqtt
import json


HOST = "localhost"
PORT = 4223
UID = "vBK" # Change XYZ to the UID of your LCD 20x4 Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_lcd_20x4 import BrickletLCD20x4

	
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("lcd/write")

def on_message(client, userdata, msg):
    message=  msg.payload.decode()
    print(message)
	
    text = json.loads(message)
	
    ipcon = IPConnection() # Create IP connection
    lcd = BrickletLCD20x4(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
    if text['type']=='write':
       lcd.clear_display()
       lcd.write_line(0, 0, text['line1'])
       lcd.write_line(1, 0, text['line2'])
       lcd.write_line(2, 0, text['line3'])
       lcd.write_line(3, 0, text['line4'])
    if text['type']=='off':
       lcd.backlight_off()
    if text['type']=='on':
       lcd.backlight_on()
    ##raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
  

    
client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()