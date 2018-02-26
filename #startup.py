import subprocess
from time import sleep

#exec("home/pi/shipping-logger/mvdata.py")
exec(open("/home/pi/shipping-logger/mvdata.py").read())

y=(0.1)
subprocess.Popen(["python3", '/home/pi/shipping-logger/#logger_active.py'])
sleep(y)
subprocess.Popen(["python", '/home/pi/shipping-logger/#display.py'])
sleep (y)
subprocess.Popen(["python", '/home/pi/shipping-logger/#climate.py'])
sleep (y)

