#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time


HOST = "localhost"
PORT = 4223
UID = "DeD" # Change XYZ to the UID of your Humidity Bricklet 2.0

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    h = BrickletHumidityV2(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
    h.set_status_led_config(1)
    # Get current humidity
    humidity = h.get_humidity()
    temperature = h.get_temperature()
    out={'humidity':humidity , 'temperature': temperature}
    print(json.dumps(out))
    time.sleep(0.05)
    h.set_status_led_config(0)
    time.sleep(0.05)
    h.set_status_led_config(1)
    time.sleep(0.05)
    h.set_status_led_config(0)


