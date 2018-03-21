import time
import datetime
import os
import psutil
import subprocess

import Adafruit_GPIO.SPI as SPI
import lib.SSD1306
Adafruit_SSD1306 = lib.SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#import image

start_time = datetime.datetime.now()

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


######################
from lib.adxl345 import ADXL345
import RPi.GPIO as GPIO
import os
from lib.bme280 import *
import math

adxl345 = ADXL345()


#######################

calfile = "/home/pi/shipping-logger/res/cal.py"

######################

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

def display(firstline, secondline = "", thirdline = "", fourthline = ""):

    # Initialize library.
    #disp.begin()

    # Clear display.
    #disp.clear()
    #disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    #font = ImageFont.load_default()
    font = ImageFont.truetype(font="/home/pi/shipping-logger/res/NotoMono-Regular.ttf", size=10, index=0, encoding='')

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    draw.text((x, top),    firstline,  font=font, fill=255, size=2)
    draw.text((x, top+8),  secondline, font=font, fill=255)
    draw.text((x, top+16), thirdline,  font=font, fill=255)
    draw.text((x, top+24), fourthline,  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()


def calibrate(side, avg = 5000):
    dur = 5

    msg = "Place on " + str(side)
    msg2 = "You have " + str(dur) + " seconds"
    display(msg, msg2)
    time.sleep(dur)

    display("Measuring...", "Do not move")
    x = 0
    y = 0
    z = 0
    for i in xrange(0,avg):
        #meas = "Measurement " + str(i) + " of " + str(avg)
        #display("Measuring...", "Do not move", meas)
        axes = adxl345.getAxes(True)
        x = x + axes['x']
        y = y + axes['x']
        z = z + axes['z']
    x_avg = x / avg
    y_avg = y / avg
    z_avg = z / avg

    return [x_avg, y_avg, z_avg]


# Initialize program
display("Welcome!","Startup successful.")
time.sleep(1)
#display("Calibration?","For calibrating,", "shake now.")
#time.sleep(5)

# start calibration by shaking
cal = False
for i in xrange(0,5):
    duration = time.time() + 1
    display("Calibration?","For calibrating,", "shake now.", (str(5-i) + " seconds left"))
    while time.time() < duration:
        axes = adxl345.getAxes(True)
        val = axes['x'] + axes['y'] + axes['z']
        if val > 3:
            cal = True

if os.path.exists(calfile) == False:
    display("Not calibrated yet", "First calibraion", "is necessary")
    cal = True
    time.sleep(2)

if cal == True:
    display("Calibration starting...","Calibration starts","in one second...")
    time.sleep(1)

    # bottom
    avg = calibrate("bottom")
    x_avg1 = avg[0]
    y_avg1 = avg[1]
    #z_avg6 = avg[2]

    # left
    avg = calibrate("left")
    x_avg2 = avg[0]
    #y_avg2 = avg[1]
    z_avg2 = avg[2]

    # right
    avg = calibrate("right")
    x_avg3 = avg[0]
    #y_avg3 = avg[1]
    z_avg3 = avg[2]


    # front
    avg = calibrate("front")
    #x_avg4 = avg[0]
    y_avg4 = avg[1]
    z_avg4 = avg[2]


    # back
    avg = calibrate("back")
    #x_avg5 = avg[0]
    y_avg5 = avg[1]
    z_avg5 = avg[2]


    # top
    avg = calibrate("top")
    x_avg6 = avg[0]
    y_avg6 = avg[1]
    #z_avg6 = avg[2]


    # get averages
    x_avg_t = (x_avg1 + x_avg2 + x_avg3 + x_avg6) / 4
    y_avg_t = (y_avg1 + y_avg4 + y_avg5 + y_avg6) / 4
    z_avg_t = (z_avg2 + z_avg3 + z_avg4 + z_avg5) / 4


    # save tofile
    xx = "x_avg = " + str(x_avg_t) + "\n"
    yy = "y_avg = " + str(y_avg_t) + "\n"
    zz = "z_avg = " + str(z_avg_t) + "\n"

    file = open(calfile,"w")
    file.write("# calibration values\n")
    file.write(xx)
    file.write(yy)
    file.write(zz)
    file.close()


    #finish
    display("Ready. Calibration values:", str(x_avg_t), str(y_avg_t), str(z_avg_t))
    time.sleep(10)


display("Parcel logger", "(c) Manuel Hodrius", "Licensed under", "Create Commons")
time.sleep(1)
display("Logging starts", "Files are saved", "in subfolder", "\loggerdata")
time.sleep(1)

