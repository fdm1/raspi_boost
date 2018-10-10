from pyb00st.movehub import MoveHub
from pyb00st.constants import *

from dataclasses import dataclass
from datetime import datetime, timedelta
from time import sleep
import evdev
import threading

MY_MOVEHUB_ID = '00:16:53:A7:65:D6'
MY_BTCTRLR_HCI = 'hci0'

MY_GAMEPAD_NAME = 'nunchuk'

STOP_EVENT = threading.Event()

DAMPEN_THRESHOLD = 5
UPDATE_TIME = 200

@dataclass
class HatPosition:
    x: 0
    y: 0

    def _get(self, coordinate):
        return self.__dict__[coordinate]

    def _update(self, coordinate, value):
        self.__dict__[coordinate] = value

    def minmax(self):
        for i in ['x', 'y']:
            if self._get(i) > 0:
                self._update(i, min(self._get(i), 100))
            else:
                self._update(i, max(self._get(i), -100))

    def dampen(self, threshold=DAMPEN_THRESHOLD):
        for i in ['x', 'y']:
            if abs(self._get(i)) <= threshold:
                self._update(i, 0)

    def get_position(self):
        self.dampen()
        self.minmax()
        return (self.x, self.y)


class MotorThread(threading.Thread):

    position = HatPosition(0,0)

    left_dc = 0
    right_dc = 1
    running = False

    def __init__(self, movehub, stop_event=STOP_EVENT):
        threading.Thread.__init__(self)
        self.running = True
        self.stop_event = stop_event
        self.movehub=movehub
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
        self.movehub.run_motor_for_time(MOTOR_A, UPDATE_TIME * 2, self.left_dc)
        self.movehub.run_motor_for_time(MOTOR_B, UPDATE_TIME * 2, self.right_dc)

    def run(self):
        while self.running:
            if not self.stop_event.is_set():
                self.update_motors()
                sleep(UPDATE_TIME / 1000.0)


def get_gamepad(name=MY_GAMEPAD_NAME, timeout=30):
    start = datetime.now()
    gamepad_found = False

    print("Turn on the gamepad")
    while not gamepad_found and datetime.now() < start + timedelta(seconds=timeout):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            if MY_GAMEPAD_NAME.lower() in device.name.lower():
                my_gamepad = evdev.InputDevice(device.path)
                gamepad_found = True
        sleep(1)

    if not gamepad_found:
        print('\'{}\' not found'.format(MY_GAMEPAD_NAME))
        exit()
    else:
        print(f'Gamepad ready: {my_gamepad.name}')
        return my_gamepad


def read_input(controller, motor_thread, stop_event=STOP_EVENT):
    for event in controller.read_loop():
        if event.type == 3:
            # joystick or pad event
            if event.code == evdev.ecodes.ABS_HAT0X:
                motor_thread.position.x = event.value
            if event.code == evdev.ecodes.ABS_HAT0Y:
                motor_thread.position.y = event.value

        if event.type == 1:
            # button event
            if event.code == evdev.ecodes.BTN_Z:
                if motor_thread.running:
                    print("Stopping")
                    motor_thread.running = False
                    stop_event.set()
                else:
                    print("Restarting")
                    motor_thread.running = True
                    stop_event.clear()



def get_movehub(hub_id=MY_MOVEHUB_ID, hci=MY_BTCTRLR_HCI):
    print("Turn on MoveHub")
    movehub = MoveHub(hub_id, 'Auto', hci)
    movehub.start()
    print("MoveHub ready!")
    return movehub


def kill(stop_event=STOP_EVENT):
    stop_event.set()


def run(stop_event=STOP_EVENT):
    try:
        movehub = get_movehub()
        gamepad = get_gamepad()

        stop_event.set()

        motor_thread = MotorThread(movehub=movehub)
        motor_thread.setDaemon(True)
        motor_thread.start()

        stop_event.clear() # restart
        read_input(gamepad, motor_thread)

    finally:
        motor_thread.running = False
        kill()

if __name__ == '__main__':
    run()
