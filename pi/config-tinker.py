#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "62fTXQ" # Change XXYYZZ to the UID of your Master Brick

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_master import BrickMaster

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