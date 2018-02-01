# Logger for climate
#
# Author: Manuel Hodrius, 2018

import time
import datetime
import RPi.GPIO as GPIO
import os
from bme280 import *

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

time_prev = time.perf_counter()
runningnumber = 0
filenumber = 0
prefcycle = 0
old_millis = 0

# options for files
filenamebase = "climatedata"
subfoldername = "loggerdata"
filebreak = 10000

#for LED
light = 0

if not os.path.exists(subfoldername):
    os.makedirs(subfoldername)
    print ("folder created")
    
print ("Start logging climate")

# loop forever
while True:
    begintime = time.perf_counter()
    
    # fetch sensor values to write
    now = datetime.datetime.now()

    # update time to measure cycle time
    curr_millis = round((time.perf_counter()*1000),4)

    # creat list with values as strings
    con_list = [str(runningnumber) , "," , str(round(sensor.read_temperature(),2)) ,  "," , str(round((sensor.read_pressure()/100),2)) ,  "," , str(round(sensor.read_humidity(),2)) , "\n"]
    content = ''.join(con_list)

    # create the file name
    if (runningnumber % filebreak == 0):
        filenumber = filenumber + 1
        filedate = now.strftime("%Y-%m-%d")
        filename_list = [subfoldername , "/" , filenamebase , "_" , filedate , "_" , str(filenumber) , ".csv"]
        filename = ''.join(filename_list)

    # write to file
    file = open(filename, "a+")
    file.write(content)
    file.close()
    
    # increase running number
    runningnumber = runningnumber + 1

