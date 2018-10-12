from pyb00st.movehub import MoveHub
from pyb00st.constants import MOTOR_A, MOTOR_B

from .wheelbot import WheelBot

MY_BTCTRLR_HCI = 'hci0'

class MovehubBot(WheelBot):

    MAX_POWER = 100
    MIN_POWER = -100

    def __init__(self, movehub_id):
        self.left_motor = MOTOR_A
        self.right_motor = MOTOR_B
        self.get(hub_id=movehub_id)

    def get(self, hub_id, hci=MY_BTCTRLR_HCI):
        print("Turn on MoveHub")
        movehub = MoveHub(hub_id, 'Auto', hci)
        movehub.start()
        print("MoveHub ready!")
        self.movehub = movehub
        return self.movehub

    def run_motor_for_time(self, motor, time, power):
        if power > 0:
            self.movehub.run_motor_for_time(motor, time, min(power, self.MAX_POWER))
        else:
            self.movehub.run_motor_for_time(motor, time, max(power, self.MIN_POWER))

    def run_left_motor_for_time(self, time, power):
        self.run_motor_for_time(MOTOR_A, time, power)

    def run_right_motor_for_time(self, time, power):
        self.run_motor_for_time(MOTOR_B, time, power)
