import threading
from time import sleep

STOP_EVENT = threading.Event()

class TestThread(threading.Thread):

    val_a = 0
    val_b = 1

    def __init__(self, emergency_stop_event, name, mult=None):
        threading.Thread.__init__(self)
        self.running = True
        self.setName(name)
        self.emergency_stop_event = emergency_stop_event
        self.mult = mult or 1
        print(f"{self.name} Ready")

    def run(self):
        while self.running:
            if not self.emergency_stop_event.is_set():
                print(f"{self.name}: {self.val_a * self.mult, self.val_b * self.mult}")
                sleep(1)


def arm_threads(threads, stop_event):
    stop_event.set() # stop threads
    running_threads = {thread.name for thread in threading.enumerate()}

    for thread in threads:
        if thread not in running_threads:
            print(f"Setting up {thread}")
            thread = TestThread(stop_event, thread, threads[thread])
            thread.setDaemon(True)
            thread.start()
        else:
            print(f"Thread {thread.name} was already initiated")

THREADS = {
    'MOTOR': 1,
    'DISTANCE': -20,
}

def run(threads=THREADS, stop_event=STOP_EVENT):
    arm_threads(threads, stop_event)
    print("Clearing stop event")
    stop_event.clear() # restart
    while not stop_event.is_set():
        TestThread.val_a = TestThread.val_a + 1
        TestThread.val_b = TestThread.val_b - 1
        sleep(0.5)


def kill(stop_event=STOP_EVENT):
    stop_event.set()
