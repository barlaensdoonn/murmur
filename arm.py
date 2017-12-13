#!/usr/bin/python3
# murmur - class to represent single arm with 3 actuators
# 12/9/17
# updated: 12/13/17

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
    '''

    actuators = ['lower', 'middle', 'upper']

    def __init__(self, pins, **kwargs):
        '''we accept **kwargs here to pass in board_type if needed'''
        self.relays = self._initialize_relays(pins, **kwargs)

    def _initialize_relays(self, pins, **kwargs):
        relays = [Relay(pin, **kwargs) for pin in pins]

        return dict(zip(self.actuators, relays))

    def test_connections(self):
        for actuator in self.actuators:
            self.relays[actuator].test_connection()
