#!/usr/bin/env python

import sqlite3
import sys
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 17

def log_values(sensor_id, temp, hum):
	conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
	curs = conn.cursor()
	curs.execute("""INSERT INTO Temperatures VALUES(datetime('now', 'localtime'), (?), (?))""", (sensor_id,temp))
	curs.execute("""INSERT INTO Humidities VALUES(datetime('now', 'localtime'), (?), (?))""", (sensor_id,hum))
	conn.commit()
	conn.close()

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
if humidity is not None and temperature is not None:
	log_values("1", temperature, humidity)
else:
	log_values("1", -999, -999) 
