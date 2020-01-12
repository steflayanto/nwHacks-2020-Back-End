import pygetwindow as gw
import time
from util.activity_tracker import ActivityTracker

while True:
    top_window = gw.getActiveWindow().title.lower()

    known_apps = [' - google chrome', ' - visual studio code', ' - word', ' - one note', ' - powerpoint', ' - notepad', ' - foxit reader']
    for app in known_apps:
        if app in top_window:
            print(app[3:])
            break
    else:
        print(top_window)

    time.sleep(1)