import time

import psutil

import lib.SSD1306
Adafruit_SSD1306 = lib.SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

from lib.adxl345 import ADXL345
import math

adxl345 = ADXL345()

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

    draw.text((x, top),    firstline,  font=font, fill=255)
    #draw.text((x, top),    firstline,  font=font, fill=255, size=2)
    draw.text((x, top+8),  secondline, font=font, fill=255)
    draw.text((x, top+16), thirdline,  font=font, fill=255)
    draw.text((x, top+24), fourthline,  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()



display("Welcome!","Startup successful.","Testing axis", "for 20 seconds...")
time.sleep(2)

duration = time.time() + 20
while time.time() < duration:
    axes = adxl345.getAxes(True)
    x = "x: " + str(axes['x'])
    y = "y: " + str(axes['y'])
    z = "z: " + str(axes['z'])

    display("Testing axis...", x, y, z)
    #time.sleep(1)

display("Logging starts...","")
time.sleep(2)
