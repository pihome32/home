import time
import os

# turn on the green LED
os.system("sudo bash -c \"echo 0 > /sys/class/leds/led0/brightness\"")
os.system("sudo bash -c \"echo 0 > /sys/class/leds/led1/brightness\"")

