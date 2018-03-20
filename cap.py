#!/user/bin/env python

import RPi.GPIO as GPIO
import time

timeout = 100000
DEBUG = 1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def CapRead(inPin,outPin,cycles=1,avg=500):
    # while receive pin is LOW AND total is positive value
    count = 0

    for j in xrange(0,cycles):
        sum = 0

        # for loop for average
        for a in xrange(0,avg):

            # set Send Pin Register low
            GPIO.setup(outPin, GPIO.OUT)
            GPIO.output(outPin, GPIO.LOW)

            # set receivePin Register low to make sure pullups are off
            GPIO.setup(inPin, GPIO.OUT)
            GPIO.output(inPin, GPIO.LOW)
            GPIO.setup(inPin, GPIO.IN)

            # set send Pin High
            GPIO.output(outPin, GPIO.HIGH)

            while( GPIO.input(inPin) == GPIO.LOW and sum < timeout ):
            #while( GPIO.input(inPin) != GPIO.HIGH and sum < timeout):
                sum = sum + 1

            # set receive pin HIGH briefly to charge up fully - because the while loop above will exit when pin is ~ 2.5V
            GPIO.setup( inPin, GPIO.OUT )
            GPIO.output( inPin, GPIO.HIGH )
            GPIO.setup( inPin, GPIO.IN )

        count = count + round((float(sum)/avg),2)

    return count

    #time.sleep(2/1000)

    # clean before you leave
    GPIO.cleanup()

# loop
while True:
    cyc = CapRead(23,24,1000,2);
    print (cyc)
    #time.sleep(100/1000)
