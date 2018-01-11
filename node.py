#!/usr/bin/python3
# murmur - class to represent a single node controlling 3 arms
# 12/9/17
# updated: 1/10/17

import socket
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

    def __init__(self, **kwargs):
        '''we accept **kwargs here to pass in board_type if needed.'''

        self.hostname = self._get_hostname()
        self.arms = self._initialize_arms(**kwargs)

    def _get_hostname(self):
        return socket.gethostname().split('.')[0]

    def _initialize_arms(self, **kwargs):
        arm_zip = zip(self.host_arm_map[self.hostname], self.pin_groups)

        return {group[0]: Arm(group[1], self.hostname, **kwargs) for group in arm_zip}
