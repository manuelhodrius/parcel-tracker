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

# LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

adxl345 = ADXL345()

axes = adxl345.getAxes(True)

#sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

time_prev = time.perf_counter()
runningnumber = 0
filenumber = 0
prefcycle = 0
old_millis = 0

# options for files
filenamebase = "loggerdata"
subfoldername = "loggerdata"
filebreak = 10000

#for LED
light = 0

cycletime = 5

if not os.path.exists(subfoldername):
    os.makedirs(subfoldername)
    print ("folder created")

#for x in range (0,100):
print ("Logging started ", datetime.datetime.now())

axsum_old = 1000

axthres = 0.2

# loop forever
while True:
    begintime = time.perf_counter()

    # fetch sensor values to write
    now = datetime.datetime.now()
    axes = adxl345.getAxes(True)
    capsensor = 0

    # activate if there is movement
    axsum = axes[0] + axes[1] + axes[2]
    if (abs(axsum - axsum_old) > axthres):
        
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

        # create the file name
        if (runningnumber % filebreak == 0):
            filenumber = filenumber + 1
            filedate = now.strftime("%Y-%m-%d")
            filename_list = [subfoldername , "/" , filenamebase , "_" , filedate , "_" , str(filenumber) , ".csv"]
            filename = ''.join(filename_list)

        # write to file + flash LED
        #GPIO.output(18,GPIO.HIGH)
        file = open(filename, "a+")
        file.write(content)
        file.close()
        #GPIO.output(18,GPIO.LOW)

        #flash LED
        if (runningnumber % 50 == 0):
            if (light == 1):
                light = 0
                GPIO.output(18,GPIO.LOW)
            else:
                light = 1
                GPIO.output(18,GPIO.HIGH)
        runningnumber = runningnumber + 1
        axsum_old = axsum
    else:
        continue

