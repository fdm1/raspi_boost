from datetime import datetime, timedelta
from time import sleep
import evdev
import pygatt


class Gamepad:

    def __init__(self, name, timeout=30):
        self._get_gamepad(name, timeout)

    def _get_gamepad(self, name, timeout):
        start = datetime.now()
        gamepad_found = False

        print(f"Turn on the {name} gamepad")
        while datetime.now() < start + timedelta(seconds=timeout):
            devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
            for device in devices:
                if name.lower() in device.name.lower():
                    self.gamepad = evdev.InputDevice(device.path)
                    print(f'Gamepad ready: {self.gamepad.name}')
                    return
            sleep(1)

        print('\'{}\' not found'.format(name))
        exit()


    def read_input(self, motor_thread):
        for event in self.gamepad.read_loop():
            if event.type == 3:
                # joystick or pad event
                if event.code == evdev.ecodes.ABS_HAT0X:
                    motor_thread.position.x = event.value
                if event.code == evdev.ecodes.ABS_HAT0Y:
                    motor_thread.position.y = event.value

            if event.type == 1:
                # button event
                if event.code == evdev.ecodes.BTN_Z and evdev.ecodes.BTN_Z in self.gamepad.active_keys():
                    if motor_thread.paused:
                        print("Unpausing")
                        motor_thread.unpause()
                    else:
                        print("Pausing")
                        motor_thread.pause()

    def shutdown(self):
        # hack figured out - the wiimote will disconnect if the bluetooth adapter restarts
        bt_adapter = pygatt.GATTToolBackend(hci_device="hci0")
        bt_adapter.start()
        bt_adapter.stop()
