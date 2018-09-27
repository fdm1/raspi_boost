#!/usr/bin/env python3

from pyb00st.movehub import MoveHub
from pyb00st.constants import *
from connect import connect
from time import sleep

MY_BTCTRLR_HCI = 'hci0'


try:
    mymovehub = connect()
    mymovehub.subscribe_all()
    mymovehub.listen_hubtilt(MODE_HUBTILT_BASIC)

    while True:
        sleep(0.2)
        if mymovehub.last_hubtilt in TILT_BASIC_VALUES:
            print(TILT_BASIC_TEXT[mymovehub.last_hubtilt])

finally:
    mymovehub.stop()
