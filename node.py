#!/usr/bin/python3
# murmur - class to represent a single node controlling 3 arms
# 12/9/17
# updated: 12/9/17

from arm import Arm


class Node(object):

    pin_groupings = {
        'left_arm': [17, 27, 22],
        'middle_arm': [5, 6, 13],
        'right_arm': [6, 20, 21]
    }

    def __init__(self):
        pass
