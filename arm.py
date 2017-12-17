#!/usr/bin/python3
# murmur - class to represent single arm with 3 actuators
# 12/9/17
# updated: 12/13/17

from datetime import timedelta
from relay import Relay


class Arm(object):
    '''
    Arm.relays dictionary returned from _initialize_relays() is formatted as follows,
    where Relay(pins[i]) represents an initiated relay object:

    self.relays = {
        'lower': Relay(pins[0]),
        'middle': Relay(pins[1]),
        'upper': Relay([pins[2])
    }

    total_time = total amount of time in seconds that an arm takes to go through its movement sequence
    ratio = ratio expressing each actuator's piece of total_time

    '''

    total_time = timedelta(seconds=180)

    actuators = ['lower', 'middle', 'upper']
    ratio = [1, 3, 2]
    ratio_total = sum(ratio)
    seconds_split = [i/ratio_total * total_time.seconds for i in ratio]

    def __init__(self, pins, **kwargs):
        '''
        we accept **kwargs here to pass in board_type if needed. also pins should be
        a list of 3 ints corresponding to GPIO pins to assign to the arm's relays
        '''

        self.relays = self._initialize_relays(pins, **kwargs)

    def _initialize_ratio(self):
        pass

    def _initialize_relays(self, pins, **kwargs):
        relays = [Relay(pin, **kwargs) for pin in pins]

        return dict(zip(self.actuators, relays))

    def test_connections(self):
        for actuator in self.actuators:
            self.relays[actuator].test_connection()

    def run_forward(self):
        pass
