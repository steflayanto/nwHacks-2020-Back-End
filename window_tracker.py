import pygetwindow as gw
import time, threading
from util.activity_tracker import ActivityTracker
from collections import Counter
import json, requests

total_tracker = Counter()

tracker = ActivityTracker()

url = "https://httpbin.org/post"

def update_tracker(top_window):
    known_apps = [' - visual studio code', ' - word', ' - one note', ' - powerpoint', ' - notepad', ' - foxit reader']
    if ' - google chrome' in top_window:
        title = 'chrome-'
        if 'youtube - ' in top_window:
            title += 'youtube'
        elif 'facebook - ' in top_window:
            title += 'facebook'
        elif 'instagram - ' in top_window:
            title += 'instagram'
        elif 'messenger - ' in top_window:
            title += 'messenger'
        elif 'whatsapp - ' in top_window:
            title += 'whatsapp'
        else:
            title += 'work'
        
        tracker.start_activity(title)

    elif 'slack |' in top_window:
        tracker.start_activity('slack')

    else:
        for app in known_apps:
            if app in top_window:
                tracker.start_activity(app[3:])
                break
        else:
            tracker.start_activity(top_window)

prev_window = None
update_timer = time.time()


while True:
    if time.time() - update_timer > 10:
        update_timer = time.time()

        print("Updating to total tracker")
        activities_dict = tracker.get_activities_dict()
        total_tracker.update(activities_dict)
        tracker.clear()
        print(total_tracker)
        
        print("Sending Json")
        r = requests.post(url, data=json.dumps(activities_dict))
        print(r.text)
    
    window = gw.getActiveWindow()
    if not window or not window.title:
        continue
    top_window = window.title.lower()
    # if prev_window != top_window:
    update_tracker(top_window)
        # prev_window = top_window
    time.sleep(0.5)