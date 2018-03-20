import os
import shutil

from variables import subfoldername, pathbase

# set source and destination paths
path = pathbase + "/" + subfoldername

# new folder name
foldername_new = "o_" + subfoldername
path_new = pathbase + "/" + "o_" + foldername_new

if os.path.exists(path):
    # see if it already exists and rename the new folder
    while os.path.exists(path_new):
        foldername_new = "o_" + foldername_new
        path_new = pathbase + "/" + foldername_new

    os.rename(path, path_new)

print("old folder renamed")
