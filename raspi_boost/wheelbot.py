from abc import ABC, abstractmethod

class WheelBot(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def run_left_motor_for_time(self, time, power):
        pass

    @abstractmethod
    def run_right_motor_for_time(self, time, power):
        pass