import threading
from time import sleep
from .hat_position import HatPosition

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

    def convert_position_to_motor_values(self):
        x, y = self.position.get_position()
        # wheelbot limits min/max. This is still going over limit, so not ideal
        self.left_dc = y+x
        self.right_dc = y-x

    def update_motors(self):
        self.wheelbot.run_right_motor_for_time(UPDATE_TIME * 2, self.left_dc)
        self.wheelbot.run_left_motor_for_time(UPDATE_TIME * 2, self.right_dc)

    def run(self):
        print(f"self.running = {self.running}")
        print(f"self.stop_event.is_set() = {self.stop_event.is_set()}")
        while self.running:
            self.convert_position_to_motor_values()
            print(f"position={self.position}, motors={(self.left_dc, self.right_dc)}")
            if not self.stop_event.is_set():
                self.update_motors()

            sleep(UPDATE_TIME / 1000.0)


    def unpause(self):
        self.paused = False
        self.running = True
        self.stop_event.clear()

    def pause(self):
        self.paused = True
        self.stop_event.set()

    def kill(self):
        self.pause()
        self.running = False
