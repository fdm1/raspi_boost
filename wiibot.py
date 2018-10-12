from raspi_boost.gamepad import Gamepad
from raspi_boost.motor_thread import MotorThread
from raspi_boost.movehub_bot import MovehubBot

def run():
    try:
        movehub = MovehubBot('00:16:53:A7:65:D6')
        gamepad = Gamepad('nunchuk')

        motor_thread = MotorThread(wheelbot=movehub)
        motor_thread.setDaemon(True)
        motor_thread.start()

        motor_thread.unpause()

        gamepad.read_input(motor_thread)

    finally:
        motor_thread.kill()

if __name__ == '__main__':
    run()
