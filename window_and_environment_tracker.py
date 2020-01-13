import pygetwindow as gw
import time, threading
from util.activity_tracker import ActivityTracker
from util.ambient_noise import AmbientNoise
from collections import Counter
import json, requests
import cv2

distracted_apps = ["chrome-youtube", "chrome-facebook", "chrome-instagram", "chrome-messenger", "chrome-whatsapp", "slack"]

total_tracker = Counter()

tracker = ActivityTracker()

# url = "https://httpbin.org/post"
url = r"http://localhost:5000/data"

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

update_timer = time.time()

mic = AmbientNoise()

while True:
    if time.time() - update_timer > 10:
        update_timer = time.time()

        print("Updating to total tracker")
        activities_dict = tracker.get_activities_dict()
        total_tracker.update(activities_dict)
        tracker.clear()
        print(total_tracker)
        
        data = dict()
        distracted_dict = dict()
        focused_dict = dict()

        for app, duration in activities_dict.items():
            if app in distracted_apps:
                distracted_dict[app] = duration
            else:
                focused_dict[app] = duration
        data["distracted"] = distracted_dict
        data["focused"] = focused_dict

        print("Getting ambient noise")
        db = mic.read()
        data["noise"] = db
        """
        print("Getting ambient light")
        cap = cv2.VideoCapture(0)
        assert cap.isOpened()
        ret, frame = cap.read(0)
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            data["light"] = cv2.mean(gray)[0]
        cap.release()
"""     
        data["light"] = 221

        print("Sending Json")

        try:
            headers = {'Content-type': 'application/json'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            print(json.dumps(data))
        except:
            print("Failed to post")
            
    
    window = gw.getActiveWindow()
    if not window or not window.title:
        continue
    top_window = window.title.lower()
    # if prev_window != top_window:
    update_tracker(top_window)
        # prev_window = top_window
    time.sleep(0.5)