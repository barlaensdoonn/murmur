#!/usr/bin/python3
# murmur - class to represent single arm with 3 actuators
# 12/9/17
# updated: 1/16/18

import logging
from datetime import timedelta
from relay import relay  # nested relay repo from here: https://github.com/barlaensdoonn/relay


class Arm(object):
    '''
    Arm.actuators dictionary returned from _initialize_actuators() is formatted as follows,
    where Relay(pins[i]) represents an initiated relay object:

    self.actuators = {
        'low': Relay(pins[0]),
        'mid-A': Relay(pins[1]),
        'mid-B': Relay([pins[2]),
        'tip-top': Relay([pins[3])
    }

    total_time = total amount of time in seconds that an arm takes to go through its movement sequence
    ratio = ratio expressing each actuator's piece of total_time

    '''

    # total_time = timedelta(seconds=180)
    # ratio = [1, 3, 2]
    # ratio_total = sum(ratio)
    # seconds_split = [i/ratio_total * total_time.seconds for i in ratio]

    def __init__(self, arm, pins, **kwargs):
        '''
        we accept **kwargs here to pass in board_type if needed.
        pins should be a list of ints corresponding to GPIO pins to control actuators
        '''

        self.arm = arm
        self.logger = self._initialize_logger()
        self.actuators = self._initialize_actuators(pins, **kwargs)

    def _initialize_logger(self):
        logger = logging.getLogger(self.arm)
        logger.info('arm {} logger instantiated'.format(self.arm))

        return logger

    def _initialize_ratio(self):
        pass

    def _initialize_actuators(self, pins, **kwargs):
        self.logger.info('initializing actuators on GPIO pins {}, {}, {}, {}'.format(*pins))
        actuators = [relay.Relay(pin, **kwargs) for pin in pins]

        return dict(zip(self.actuators, actuators))

    def test_connections(self):
        '''utility method for debugging'''

        test_order = ['low', 'mid-A', 'mid-B', 'top']

        for actuator in test_order:
            self.logger.debug('testing {actuator} relay connection on pin {pin}'.format(actuator=actuator, pin=self.actuators[actuator].pin))
            self.actuators[actuator].test_connection()

    def activate(self, actuator):
        self.logger.info('activating {}'.format(actuator))
        self.actuators[actuator].activate()

    def deactivate(self, actuator):
        self.logger.info('deactivating {}'.format(actuator))
        self.actuators[actuator].deactivate()
