#!/usr/bin/python3
# murmur - class to represent a single node controlling 3 arms
# 12/9/17
# updated: 1/10/17

import socket
from arm import Arm


class Node(object):

    pin_groupings = {
        'left_arm': [4, 17, 27, 22],
        'middle_arm': [6, 13, 19, 26],
        'right_arm': [12, 16, 20, 21]
    }

    def __init__(self, **kwargs):
        '''we accept **kwargs here to pass in board_type if needed.'''

        self.hostname = self._get_hostname()
        self.arms = {key: Arm(self.pin_groupings[key], self.hostname, **kwargs) for key in self.pin_groupings.keys()}

    def _get_hostname(self):
        return socket.gethostname().split('.')[0]
