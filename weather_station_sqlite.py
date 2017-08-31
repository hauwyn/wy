#!/usr/bin/python
import os
from sense_hat import SenseHat
import time
import sys
import sqlite3
from datetime import datetime

db = "/home/pi/Desktop/weather.db"
#db = "weather.db"

connection = sqlite3.connect(db)
#with sqlite3.connect(db) as connection:
c = connection.cursor()
c.execute( """ CREATE TABLE IF NOT EXISTS weather_table(
                                        Date text,
                                        Temp float,
                                        Humidity float,
                                        Pressure float
                                    )""")

def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=","").replace("'C\n",""))
    return(t)


try:
    while True:
        sense = SenseHat()
        sense.clear()
        t1 = sense.get_temperature_from_humidity()
        t2 = sense.get_temperature_from_pressure()
        t_cpu = get_cpu_temp()
        temp = (t1 + t2 ) / 2
        temp = temp-((t_cpu-temp) / 0.8)
        temp = round(temp, 1)
        print("Temperature:", temp)
        
        humidity = sense.get_humidity() + 20
        humidity = round(humidity, 1)
        print("Humidity:", humidity)

        pressure = sense.get_pressure()
        pressure = round(pressure, 1)
        print("Pressure:", pressure)
        
        date = datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        print ("date:", date)
    
        with sqlite3.connect(db) as connection:
            c = connection.cursor()
            c.execute("INSERT INTO weather_table VALUES(?,?,?,?);", (date,temp,humidity,pressure))
            
except KeyboardInterrupt:
    pass 
               

