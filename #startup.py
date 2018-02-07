import subprocess
from time import sleep

y=(0.1)
subprocess.Popen(["python3", '/home/pi/shipping-logger/#logger.py'])
sleep(y)
subprocess.Popen(["python", '/home/pi/shipping-logger/#display.py'])
sleep (y)
subprocess.Popen(["python", '/home/pi/shipping-logger/#climate.py'])
sleep (y)

