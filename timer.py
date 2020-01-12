import time

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

timer1 = Timer()

timer2 = Timer()

timer1.start()
time.sleep(1)
timer2.start()
time.sleep(5)
timer1.stop()
timer2.stop()

print(timer1.value())
print(timer2.value())