import pygetwindow as gw
import time, threading
from util.activity_tracker import ActivityTracker
from collections import Counter

total_tracker = Counter()

tracker = ActivityTracker()

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

def update_total_tracker():
    print("Updating to total tracker")    
    total_tracker.update(tracker.get_activities_dict())
    tracker.clear()
    print(total_tracker)

prev_window = None
update_timer = time.time()


while True:
    if time.time() - update_timer > 10:
        update_total_tracker()
        update_timer = time.time()
    
    window = gw.getActiveWindow()
    if not window or not window.title:
        continue
    top_window = window.title.lower()
    # if prev_window != top_window:
    update_tracker(top_window)
        # prev_window = top_window
    time.sleep(0.5)