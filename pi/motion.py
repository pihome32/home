#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
HOST = "localhost"
PORT = 4223
UID = "EyH" # Change XYZ to the UID of your Motion Detector Bricklet 2.0

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2


loop = 10
# Callback function for motion detected callback
def cb_motion_detected():
    client = mqtt.Client()
    client.connect("localhost",1883,60)
    client.publish("motion/detected", "");
    client.disconnect();

# Callback function for detection cycle ended callback
def cb_detection_cycle_ended():
    print("Detection Cycle Ended (next detection possible in ~2 seconds)")
    loop = 10
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    md = BrickletMotionDetectorV2(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected
    md.set_sensitivity(100)
    # Register motion detected callback to function cb_motion_detected
    md.register_callback(md.CALLBACK_MOTION_DETECTED, cb_motion_detected)

    # Register detection cycle ended callback to function cb_detection_cycle_ended
    md.register_callback(md.CALLBACK_DETECTION_CYCLE_ENDED, cb_detection_cycle_ended)
    while loop> 0:
	    
       loop = 10
    ipcon.disconnect()