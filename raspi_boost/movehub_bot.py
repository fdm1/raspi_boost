from pyb00st.movehub import MoveHub
from pyb00st.constants import MOTOR_A, MOTOR_B

from wheelbot import WheelBot

MY_MOVEHUB_ID = '00:16:53:A7:65:D6'
MY_BTCTRLR_HCI = 'hci0'

class MovehubBot(WheelBot):

    def __init__(self):
        self.left_motor = MOTOR_A
        self.right_motor = MOTOR_B
        self.get()

    def get(self, hub_id=MY_MOVEHUB_ID, hci=MY_BTCTRLR_HCI):
        print("Turn on MoveHub")
        movehub = MoveHub(hub_id, 'Auto', hci)
        movehub.start()
        print("MoveHub ready!")
        self.movehub = movehub
        return self.movehub

    def run_left_motor_for_time(self, time, power):
        self.movehub.run_motor_for_time(MOTOR_A, time, power)

    def run_right_motor_for_time(self, time, power):
        self.movehub.run_motor_for_time(MOTOR_B, time, power)