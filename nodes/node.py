#!/usr/bin/python3
# murmur - class to represent a single node controlling 3 arms
# 12/9/17
# updated: 6/16/18

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

    def _modify_pin_groups(self):
        '''
        change murmur04's last pin_group, replacing GPIO pin 16 with 25.
        this is due to a wiring fault at Mystic and should be corrected in later iterations
        '''

        if self.hostname == 'murmur04':
            self.logger.info('modifying last pin group to [12, 25, 20, 21]')
            self.pin_groups[-1] = [12, 25, 20, 21]

    def _intercept_d_low(self, arm, actuator):
        '''
        intercept a message to fire D low, and return F top
        this is a hack to work around a ghost in the machine. we repurpose the F top
        relay - which is not being used - and use it to fire D low.
        '''
        print('inside _intercept_d_low() method')
        print('arm: {}, actuator: {}'.format(arm, actuator))
        if arm == 'D' and actuator == 'low':
            self.logger.info('replacing D low with F top')
            return ('F', 'low')
        else:
            return (arm, actuator)

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
        '''
        this is called in the receive module by the TCP server when a valid message is received.
        specifically it's called by the TCPHandler class in its handle() method after the msg is parsed
        '''

        try:
            # NOTE: this should be replaced in future iterations. this is a hack
            # to work around a failed relay, we repurpose F top to use for D low
            string_arm, string_actuator = self._intercept_d_low(action['arm'], action['actuator'])
            arm = self.arms[string_arm]
            actuator = string_actuator
            print('after intercept')
            print('arm: {}, actuator: {}'.format(arm, actuator))

            activate = action['activate']

            if activate:
                arm.actuators[actuator].activate()
            else:
                arm.actuators[actuator].deactivate()
        except TypeError:
            self.logger.warning('received improperly formatted message {}, ignoring...'.format(action))
        except KeyError:
            self.logger.error('invalid command received, ignoring...')
