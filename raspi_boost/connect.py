from pyb00st.movehub import MoveHub
from pyb00st.constants import *

MY_MOVEHUB_ID = '00:16:53:A7:65:D6'
MY_BTCTRLR_HCI = 'hci0'

def initialize(hub):
    pass
    hub.subscribe_all()
    for port in [PORT_A, PORT_B, PORT_C, PORT_D]:
        hub.listen_angle_sensor(port)

    for motor in [MOTOR_A, MOTOR_B, MOTOR_C, MOTOR_D]:
        hub.run_motor_for_time(motor, 5, 5)
        hub.run_motor_for_time(motor, 5, -5)

    angle_status(hub)


# would be good to be able to pass starting angles
def connect():
    hub = MoveHub(MY_MOVEHUB_ID, 'Auto', MY_BTCTRLR_HCI)
    hub.start()
    print("connected to {}".format(hub.get_name()))
    initialize(hub)
    return hub


# this is reporting relative start
def angle_status(hub):
    print("""
hub initialized:

angles:
    A: {}
    B: {}
    C: {}
    D: {}
""".format(hub.last_angle_A, hub.last_angle_B, hub.last_angle_C, hub.last_angle_D))

