# Logger for parcel shippings
#
# Author: Manuel Hodrius, 2018

# TODO
# Import capsensor!

from lib.adxl345 import ADXL345
import time
import datetime
import RPi.GPIO as GPIO
import os
from lib.bme280 import *

# Setup database
import sqlite3
sqlite_file = 'loggerdata.sqlite'
table_name = 'loggerdata'

# LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

adxl345 = ADXL345()

axes = adxl345.getAxes(True)

#sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

#time_prev = time.perf_counter()
runningnumber = 0
filenumber = 0
prefcycle = 0
old_millis = 0

#for LED
light = 0

cycletime = 5

#for x in range (0,100):
print ("Logging started ", datetime.datetime.now())

#connect to db
#conn = sqlite3.connect(sqlite_file)
#c = conn.cursor()


# loop forever
while True:
    #begintime = time.perf_counter()

    # fetch sensor values to write
    now = datetime.datetime.now()
    axes = adxl345.getAxes(True)
    capsensor = 0

    # update time to measure cycle time
    curr_millis = round((time.perf_counter()*1000),4)

    # creat list with values as strings
    con_list = [str(runningnumber) , "," , str(curr_millis) , "," ,
                now.strftime("%Y/%m/%d,%H:%M:%S") , "," ,
                str(capsensor) , "," ,
                str(axes['x']) , "," , str(axes['y']) , "," , str(axes['z']) , "," ,
                #str(round(sensor.read_temperature(),2)) ,  "," , str(round((sensor.read_pressure()/100),2)) ,  "," , str(round(sensor.read_humidity(),2)) ,
                "\n"]
    content = ''.join(con_list)

    # write to database
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute("INSERT OR IGNORE INTO {tn} \
           (counter, timestamp, date, time, cap, x, y, z) \
            VALUES ({cou}, {timst}, '{dat}', '{tim}', {cap}, {x}, {y}, {z})".\
            format(tn=table_name, cou=runningnumber, timst=curr_millis, dat=now.strftime("%Y/%m/%d"), tim=now.strftime("%H:%M:%S"), cap=capsensor, x=axes['x'], y=axes['y'], z=axes['z']))
    conn.commit()
    conn.close()

    #flash LED
    if (runningnumber % 50 == 0):
        if (light == 1):
            light = 0
            GPIO.output(18,GPIO.LOW)
        else:
            light = 1
            GPIO.output(18,GPIO.HIGH)

    # console log activity <-- deactivate for lower cycle times!
    #print(content)
    #if (runningnumber % 100 == 0):
        #print (runningnumber)

    # intelligent wait
    """endtime = time.perf_counter()
    duration = endtime - begintime
    sleeptime = (cycletime/1000) - duration
    if (sleeptime > 0):
        #print(sleeptime/1000)
        time.sleep(sleeptime)
    old_millis = curr_millis"""

    # increase running number
    runningnumber = runningnumber + 1

