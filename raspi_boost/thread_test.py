from dataclasses import dataclass
from datetime import datetime, timedelta
from time import sleep
import evdev
import threading

from movehub_bot import MovehubBot
from motor_thread import MotorThread


MY_GAMEPAD_NAME = 'nunchuk'


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


def read_input(controller, motor_thread):
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
                    motor_thread.pause()
                else:
                    print("Restarting")
                    motor_thread.unpause()



def run():
    try:
        movehub = MovehubBot()
        gamepad = get_gamepad()


        motor_thread = MotorThread(wheelbot=movehub)
        motor_thread.setDaemon(True)
        motor_thread.start()

        motor_thread.unpause()

        read_input(gamepad, motor_thread)

    finally:
        motor_thread.pause()

if __name__ == '__main__':
    run()
