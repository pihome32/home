#!/usr/bin/env python

# 2018 / MIT / Tim Clem / github.com/misterfifths
# See LICENSE for details

from __future__ import print_function

from time import sleep
from sgp30 import SGP30
from smbus2 import SMBus
from influxdb import InfluxDBClient
import pytemperature
dbname = 'home'
user = ''
password = ''
host='localhost'
port=8086

counter = 0
def sensor_config():
    print("sensor config")
    client = InfluxDBClient(host, port, user, password, dbname)
    rs = client.query('SELECT mean(*) FROM "home"."autogen"."data" WHERE time > now() - 60s AND "node"!="server"' )
    rs = list(rs.get_points())
    temp_k= pytemperature.c2k(rs[0]['mean_temperature'])
    print(temp_k)
    rel_H=rs[0]['mean_humidity']
    pressure=rs[0]['mean_pressure']
def initialise():

    sensor_config()
def main():
    smbus = SMBus(1)  # zero on some boards
    warming_up = True
    baseline_counter = 0

    initialise()
    with SGP30(smbus) as chip:
        while True:
            measurement = chip.measure_air_quality()

            # Chip returns (400, 0) for the first ~15 seconds while it warms up
            if warming_up:
                if measurement.is_probably_warmup_value():
                    print('... warming up ...')
                    sleep(1)
                    continue
                else:
                    warming_up = False


            print(measurement.co2_ppm)
            print(measurement)
            client = InfluxDBClient(host, port, user, password, dbname)
            json_body = [
            {
            "measurement": "data",
            "fields": {
                "co2": measurement.co2_ppm,
				"voc": measurement.voc_ppb,
            },
			"tags": {
			"node":"server",
			"location":"salon",
			"sensor":"sgp30",
			},
             }
            ]

            client.write_points(json_body)	

			

            # Don't take this as a complete example... read the spec sheet about how you're supposed to stash and restore the baseline, initial burn-in, humidity compensation, *and how you need to sample every second to maintain accurate results*
            baseline_counter = baseline_counter + 1
            if baseline_counter % 100 == 0:
                sensor_config()
                baseline_counter = 0
                baseline = chip.get_baseline()
                print('>> Baseline:', baseline)

            sleep(10)

if __name__ == '__main__':
    main()




	
