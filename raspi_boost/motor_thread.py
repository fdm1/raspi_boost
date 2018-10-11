import threading
from time import sleep
from hat_position import HatPosition

UPDATE_TIME = 200
STOP_EVENT = threading.Event()

class MotorThread(threading.Thread):

    position = HatPosition(0,0)

    left_dc = 0
    right_dc = 1
    running = False

    def __init__(self, wheelbot, stop_event=STOP_EVENT):
        threading.Thread.__init__(self)
        self.stop_event = stop_event
        self.pause()
        self.wheelbot = wheelbot
        print(f"MotorThread Ready")

    def update_motors(self):
        x, y = self.position.get_position()
        print(f"({x}, {y})")
        if x == 0:
            self.left_dc = x
            self.right_dc = y
        if x > 0:
            self.left_dc = x
            if y >= 0:
                self.right_dc = (y - x)
            else:
                self.right_dc = (y + x)
        else:
            self.right_dc = x
            if y >= 0:
                self.left_dc = (y - x)
            else:
                self.left_dc = (y + x)
        self.wheelbot.run_right_motor_for_time(UPDATE_TIME * 2, self.left_dc)
        self.wheelbot.run_left_motor_for_time(UPDATE_TIME * 2, self.right_dc)

    def run(self):
        while self.running:
            if not self.stop_event.is_set():
                self.update_motors()
                sleep(UPDATE_TIME / 1000.0)


    def unpause(self, stop_event=STOP_EVENT):
        self.running = True
        stop_event.clear()

    def pause(self, stop_event=STOP_EVENT):
        self.running = False
        stop_event.set()