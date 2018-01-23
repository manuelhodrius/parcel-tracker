import subprocess
from time import sleep

y=(0.1)
subprocess.Popen(["python3", 'parcel-tracker/#logger.py'])
sleep(y)
subprocess.Popen(["python", 'parcel-tracker/#display.py'])
sleep (y)
