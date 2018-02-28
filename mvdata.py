import os
import shutil

# set source and destination paths
foldername = "loggerdata"
path = "/" + foldername

# new folder name
foldername_new = "o_" + foldername
path_new = "/" + foldername_new

if os.path.exists(path):
    # see if it already exists and rename the new folder
    while os.path.exists(path_new):
        foldername_new = "o_" + foldername_new
        path_new = "/" + foldername_new

    os.rename(path, path_new)

print("old folder renamed")
