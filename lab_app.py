from flask import Flask, render_template, request, redirect, url_for
import time
import datetime
import arrow

app = Flask(__name__)
app.debug = True


@app.route("/")
def root():
    return redirect(url_for('lab_env_db'))

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

@app.route("/lab_env_db", methods=['GET'])
def lab_env_db():
    temperatures, humidities, timezone, from_date_str, to_date_str = get_records()
    print temperatures[0]

    time_adjusted_temperatures = []
    time_adjusted_humidities   = []
    for temp,hum in zip(temperatures,humidities):
        local_timedate = arrow.get(temp[0], "YYYY-MM-DD HH:mm").to(timezone)
        time_adjusted_temperatures.append([local_timedate.format('YYYY-MM-DD HH:mm'), round(temp[2],2)])
        local_timedate = arrow.get(hum[0], "YYYY-MM-DD HH:mm").to(timezone)
        time_adjusted_humidities.append([local_timedate.format('YYYY-MM-DD HH:mm'), round(hum[2],2)])
    return render_template("lab_env_db.html", temp       = time_adjusted_temperatures, 
                                              hum        = time_adjusted_humidities,
                                              from_date  = from_date_str,
                                              to_date    = to_date_str,
                                              temp_items = len(temperatures),
                                              hum_items  = len(humidities))

def get_records():
    import sqlite3
    from_date_str = request.args.get('from',time.strftime("%Y-%m-%d 00:00"))
    to_date_str   = request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))
    timezone      = request.args.get('timezone','Etc/UTC')
    range_h_form  = request.args.get('range_h','')
    range_h_int   = "nan"

    try:
        range_h_int = int(range_h_form)
    except:
        print "range_h_form is not a number"

    if not validate_date(from_date_str):
        from_date_str = time.strftime("%Y-%m-%d 00:00")
    if not validate_date(to_date_str):
        to_date_str   = time.strftime("%Y-%m-%d %H:%M")

    from_date_obj = datetime.datetime.strptime(from_date_str, '%Y-%m-%d %H:%M')
    to_date_obj   = datetime.datetime.strptime(to_date_str, '%Y-%m-%d %H:%M')

    if isinstance(range_h_int,int):
        arrow_time_from = arrow.utcnow().replace(hours=-range_h_int)
        arrow_time_to   = arrow.utcnow()
        from_date_utc   = arrow_time_from.strftime("%Y-%m-%d %H:%M")
        to_date_utc     = arrow_time_to.strftime("%Y-%m-%d %H:%M")
        from_date_str   = arrow_time_from.to(timezone).strftime("%Y-%m-%d %H:%M")
        to_date_str     = arrow_time_to.to(timezone).strftime("%Y-%m-%d %H:%M")
    else:
        from_date_utc = arrow.get(from_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")
        to_date_utc   = arrow.get(to_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")

    query_start = 'SELECT * FROM'
    query_end   = 'WHERE rDatetime BETWEEN \"{}\" AND \"{}\" ORDER BY rDatetime DESC'.format(from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm'))

    temp_query_str = query_start + ' Temperatures ' + query_end
    hum_query_str  = query_start + ' Humidities ' + query_end

    conn = sqlite3.connect('/var/www/lab_app/lab_app.db')
    curs = conn.cursor()

    curs.execute(temp_query_str)
    temperatures = curs.fetchall()

    curs.execute(hum_query_str)
    humidities = curs.fetchall()

    conn.close()
    return [temperatures, humidities, timezone, from_date_str, to_date_str]

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
