import random, time

class Timer:
    running = False
    time_elapsed = 0
    time_started = 0

    def start(self):
        # If timer is not already running
        if not self.running:
            self.time_started = time.time()
            self.running = True
    
    def stop(self):
        #If timer is already running
        if self.running:
            self.running=False
            self.time_elapsed += time.time() - self.time_started
        return self.time_elapsed

    def value(self):
        return self.time_elapsed
    
    def reset(self):
        self.running = False
        self.time_elapsed = 0
        self.time_started = 0

activity_timers = dict()
last_activity = "productive"
activities = ["productive", "texting", "conversation", "youtube", "instagram", "messenger", "facebook", "sleeping"]

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

start_time = time.time()

while True:
    next_activity = random.choice(activities)
    activity_timers[last_activity].stop()
    activity_timers[next_activity].start()
    last_activity = next_activity
    time.sleep(random.random() * 3)
    total = 0
    for activity, timer in activity_timers.items():
        val = timer.value()
        total += val
        # print(str(activity) + ": " + str(val))
    print(total)
    print("time elapsed: " + str(time.time() - start_time))
    print("\n\n")