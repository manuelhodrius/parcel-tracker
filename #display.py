# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import os

import psutil

import Adafruit_GPIO.SPI as SPI
import SSD1306
Adafruit_SSD1306 = SSD1306

import time
import datetime

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#import image

import subprocess

start_time = datetime.datetime.now()

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

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
font = ImageFont.truetype(font="/home/pi/parcel-tracker/NotoMono-Regular.ttf", size=10, index=0, encoding='')

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
        )))

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

while True:
    now = datetime.datetime.now()

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    #cmd = "hostname -I | cut -d\' \' -f1"
    #IP = subprocess.check_output(cmd, shell = True )
    #cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    #CPU = subprocess.check_output(cmd, shell = True )
    #CPU = CPU_usage = getCPUuse()
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    cpu = "CPU " + str(psutil.cpu_percent()) + "%"
    mem = "MEM " + str(psutil.virtual_memory().used/1000000) + " MB / " + str(psutil.virtual_memory().percent) + " %"
    logtime = "RUNTIME " + str(datetime.datetime.now()-start_time)[:-7]

    # Write two lines of text.
    
    draw.text((x, top),       now.strftime("%Y/%m/%d,%H:%M:%S"),  font=font, fill=255, size=2)
    draw.text((x, top+8),     cpu, font=font, fill=255)
    draw.text((x, top+16),    mem,  font=font, fill=255)
    draw.text((x, top+24),    logtime,  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(1)
