#!/usr/bin/env python3
import subprocess
import time


# copied from https://askubuntu.com/questions/576525/is-there-any-way-to-make-ubuntu-not-to-suspend-while-a-download-in-progress/660295


#--- set suspend time below (seconds)
suspend_wait = 300
#---

#--- you can change values below, but I'd leave them as they are
speed_limit = 0      # set a minimum speed (kb/sec) to be considered a download activity
looptime = 20        # time interval between checks
download_wait = 300  # time (seconds) to wait after the last download activity before suspend is re- activated
#---

t = 0
key = ["gsettings", "get", "org.gnome.settings-daemon.plugins.power", "sleep-inactive-ac-timeout", "set"]

set_suspend = key[0]+" "+key[-1]+" "+(" ").join(key[2:4])
get_suspend = (" ").join(key[0:4])

def get_size():
    return int(subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8").split()[0])

def get(cmd):
    return subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")

check_1 = int(get("du -ks ~/Downloads").split()[0])

while True:
    time.sleep(looptime)
    try:
        check_2 = int(get("du -ks ~/Downloads").split()[0])
    except subprocess.CalledProcessError:
        pass
    speed = int((check_2 - check_1)/looptime)
    # check current suspend setting
    suspend = get(get_suspend).strip()
    if speed > speed_limit:
        # check/set disable suspend if necessary
        if suspend != "0":
            subprocess.Popen(["/bin/bash", "-c", set_suspend+" 0"])
        t = 0
    else:
        if all([t > download_wait/looptime, suspend != str(download_wait)]):
            # check/enable suspend if necessary
            subprocess.Popen(["/bin/bash", "-c", set_suspend+" "+str(suspend_wait)])
    check_1 = check_2
    t = t+1
