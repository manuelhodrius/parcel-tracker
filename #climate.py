# Logger for climate
#
# Author: Manuel Hodrius, 2018

import time
import datetime
import RPi.GPIO as GPIO
import os
from lib.bme280 import *

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

runningnumber = 0
filenumber = 0
prefcycle = 0
old_millis = 0
delay = 10

# options for files
filenamebase = "climatedata"
subfoldername = "loggerdata"
filebreak = 10000

if not os.path.exists(subfoldername):
    os.makedirs(subfoldername)
    print ("folder created")

print ("Start logging climate")

# loop forever
while True:
    # fetch sensor values to write
    now = datetime.datetime.now()

    # creat list with values as strings
    con_list = [str(runningnumber) , "," , now.strftime("%Y/%m/%d,%H:%M:%S") , "," , str(round(sensor.read_temperature(),2)) ,  "," , str(round((sensor.read_pressure()/100),2)) ,  "," , str(round(sensor.read_humidity(),2)) , "\n"]
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

    # delay for x seconds
    time.sleep(delay)

