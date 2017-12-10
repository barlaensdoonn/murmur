#!/usr/bin/python3
# murmur - class to represent single arm with 3 actuators
# 12/9/17
# updated: 12/9/17

from relay import Relay


class Arm(object):
    '''
    Arm.relays dictionary format:

    self.relays = {
        'lower': Relay(pins[0]),
        'middle': Relay(pins[1]),
        'upper': Relay([pins[2])
    }
    '''

    actuators = ['lower', 'middle', 'upper']

    def __init__(self, pins):
        self.relays = _initialize_relays(pins)

    def _initialize_relays(self, pins):
        relays = [Relay(pin) for pin in pins]

        return dict(zip(actuators, relays))

    def test_connections(self):
        for actuator in actuators:
            self.relays[actuator].test_connection()
