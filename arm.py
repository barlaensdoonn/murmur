#!/usr/bin/python3
# murmur - class to represent single arm with 3 actuators
# 12/9/17
# updated: 1/10/17

import yaml
import logging
import logging.config
from datetime import timedelta
from relay import relay  # nested relay repo from here: https://github.com/barlaensdoonn/relay


class Arm(object):
    '''
    Arm.relays dictionary returned from _initialize_relays() is formatted as follows,
    where Relay(pins[i]) represents an initiated relay object:

    self.relays = {
        'low': Relay(pins[0]),
        'mid-A': Relay(pins[1]),
        'mid-B': Relay([pins[2]),
        'tip-top': Relay([pins[3])
    }

    total_time = total amount of time in seconds that an arm takes to go through its movement sequence
    ratio = ratio expressing each actuator's piece of total_time

    '''

    total_time = timedelta(seconds=180)

    actuators = ['low', 'mid-A', 'mid-B', 'tip-top']
    ratio = [1, 3, 2]
    ratio_total = sum(ratio)
    seconds_split = [i/ratio_total * total_time.seconds for i in ratio]

    def __init__(self, arm, hostname, pins, **kwargs):
        '''
        we accept **kwargs here to pass in board_type if needed.
        pins should be a list of ints corresponding to GPIO pins to control relays
        '''

        self.arm = arm
        self.hostname = hostname
        self._initialize_logger()
        self.relays = self._initialize_relays(pins, **kwargs)

    def _get_logfile_name(self):
        return '{dir}/{hostname}.log'.format(dir='logs', hostname=self.hostname)

    def _initialize_logger(self):
        with open('log.yaml', 'r') as log_conf:
            log_config = yaml.safe_load(log_conf)

        log_config['handlers']['file']['filename'] = self._get_logfile_name()
        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger('arm')
        self.logger.info('arm {} logger instantiated'.format(self.arm))

    def _initialize_ratio(self):
        pass

    def _initialize_relays(self, pins, **kwargs):
        self.logger.info('initializing relays on GPIO pins {}, {}, {}, {}'.format(*pins))
        relays = [relay.Relay(pin, **kwargs) for pin in pins]

        return dict(zip(self.actuators, relays))

    def test_connections(self):
        '''this is a utility method to be used for debugging'''

        for actuator in self.actuators:
            self.relays[actuator].test_connection()

    def run_forward(self):
        pass
