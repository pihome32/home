#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "GKb" # Change XYZ to the UID of your LCD 128x64 Bricklet

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_lcd_128x64 import BrickletLCD128x64

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    lcd = BrickletLCD128x64(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
    lcd.set_display_configuration(14,80,0,1)
   #lcd.reset()    # Clear display
    lcd.clear_display()

    # Write "Hello World" starting from upper left corner of the screen
    lcd.write_line(0, 0, "Temperature : " )
    lcd.write_line(1, 0, "Humidity : " )

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()