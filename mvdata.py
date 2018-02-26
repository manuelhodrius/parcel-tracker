import RPi.GPIO as GPIO

import os
import shutil

# LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

# set source and destination paths
source = "/loggerdata/"
new_folder = "old_data"
path = source + new_folder

if os.path.exists(path):
    print("folder exists")
else:
    os.makedirs(path)
    print ("folder created")

files = os.listdir(source)

for f in files:
    GPIO.output(18,GPIO.HIGH)
    # split filename into root and ext
    file = os.path.splitext(f)
    root = file[0]
    ext = file[1]

    # test if the file exists
    while os.path.exists((source + new_folder + "/" + root + ext)):
        #print("rename")
        org = source + root + ext
        root = root + "_o"
        new = source + root + ext
        os.rename(org, new)

    f_from = source + root + ext
    f_to = source + new_folder + "/" + root + ext

    if not new_folder in f:
        shutil.move(f_from, f_to)
    GPIO.output(18,GPIO.LOW)

print("old files moved")
