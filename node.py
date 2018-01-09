#!/usr/bin/python3
# murmur - class to represent a single node controlling 3 arms
# 12/9/17
# updated: 1/8/17

from arm import Arm


class Node(object):

    pin_groupings = {
        'left_arm': [4, 17, 27, 22],
        'middle_arm': [5, 6, 13, 19],
        'right_arm': [12, 16, 20, 21]
    }

    def __init__(self, **kwargs):
        '''we accept **kwargs here to pass in board_type if needed.'''

        self.arms = {key: Arm(self.pin_groupings[key], **kwargs) for key in self.pin_groupings.keys()}
