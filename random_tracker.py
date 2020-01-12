import random, time
from stopwatch import Stopwatch as Timer
from util.activity_tracker import ActivityTracker


activity_timers = dict()
last_activity = "productive"
activities = ["productive", "texting", "conversation", "youtube", "instagram", "messenger", "facebook", "sleeping"]

tracker = ActivityTracker()

""""
activities["productive"]
activities["texting"]
activities["conversation"]
activities["youtube"]
activities["instagram"]
activities["messenger"]
activities["website"]
"""

for activity in activities:
    activity_timers[activity] = Timer()
    activity_timers[activity].reset()

start_time = time.time()

while True:
    next_activity = random.choice(activities)
    tracker.start_activity(next_activity)
    activity_timers[last_activity].stop()
    activity_timers[next_activity].start()
    last_activity = next_activity
    time.sleep(random.random() * 3)
    total = 0
    for activity, timer in activity_timers.items():
        val = timer.duration
        total += val
        # print(str(activity) + ": " + str(val))
    tracker.print_activities()
    print(tracker.get_total_time())
    print("time elapsed: " + str(time.time() - start_time))
    print("\n\n")