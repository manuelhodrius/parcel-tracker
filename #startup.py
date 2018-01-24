import subprocess
from time import sleep

y=(0.1)
subprocess.Popen(["python3", '/#logger.py'])
sleep(y)
subprocess.Popen(["python", '#display.py'])
sleep (y)
