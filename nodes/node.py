#!/usr/bin/python3
# murmur - class to represent a single node controlling 3 arms
# 12/9/17
# updated: 1/16/18

import logging
from arm import Arm


class Node(object):
    '''
    Node.arms dictionary returned from _initialize_arms() is formatted as follows,
    where Arm(pin_groups[i]) represents an initiated Arm controlling 4 relays:

    self.arms = {
        'A': Arm(pin_groups[0]),
        'B': Arm(pin_groups[1]),
        'C': Arm(pin_groups[2])
    }
    '''

    host_arm_map = {
        'murmur01': ['A', 'B', 'C'],
        'murmur02': ['D', 'E', 'F'],
        'murmur03': ['G', 'H', 'J'],
        'murmur04': ['K', 'L', 'M']
    }

    pin_groups = [[4, 17, 27, 22], [6, 13, 19, 26], [12, 16, 20, 21]]

    def __init__(self, hostname, **kwargs):
        '''we accept **kwargs here to pass in board_type if needed.'''

        self.hostname = hostname
        self.logger = self._initialize_logger()
        self.arms = self._initialize_arms(**kwargs)

    def _initialize_logger(self):
        logger = logging.getLogger('node')
        logger.info('node logger instantiated')

        return logger

    def _initialize_arms(self, **kwargs):
        '''
        the for loop and return statement can be replaced with this more unreadable one-liner:
        return {arm: Arm(pins, self.hostname, **kwargs) for arm, pins in zip(arms, self.pin_groups)}
        '''

        arm_dict = {}
        arms = self.host_arm_map[self.hostname]
        self.logger.info('initializing arms {}, {}, and {}'.format(*arms))

        for arm, pins in zip(arms, self.pin_groups):
            arm_dict[arm] = Arm(arm, pins, **kwargs)

        return arm_dict

    def test_connections(self):
        '''utility method for debugging'''

        for arm in self.arms:
            self.arms[arm].test_connections()

    def parse_action(self, action):
        try:
            arm = self.arms[action['arm']]
            actuator = action['actuator']
            activate = action['activate']

            if activate:
                arm.actuators[actuator].activate()
            else:
                arm.actuators[actuator].deactivate()
        except TypeError:
            self.logger.warning('received improperly formatted message {}, ignoring...'.format(action))
        except KeyError:
            self.logger.error('invalid command received, ignoring...')
