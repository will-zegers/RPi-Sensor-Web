from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
	return "Hello World!"

@app.route("/lab_temp")
def lab_temp():
	import sys
	import Adafruit_DHT

	sensor = Adafruit_DHT.DHT11
	pin = 17

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	if humidity is not None and temperature is not None:
		temperature = temperature * 9/5.0 + 32
		return render_template("lab_temp.html", temp=temperature, hum=humidity)
	else:
		return render_template("no_sensor.html")

@app.route("/lab_env_db")
def lab_env_db():
	import sqlite3

	conn = sqlite3.connect('/var/www/lab_app/lab_app.db')
	curs = conn.cursor()

	curs.execute("SELECT * FROM Temperatures")
	temperatures = curs.fetchall()

	curs.execute("SELECT * FROM Humidities")
	humidities = curs.fetchall()

	conn.close()
	return render_template("lab_env_db.html", temp=temperatures, hum=humidities)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
