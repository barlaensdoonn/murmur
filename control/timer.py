#!/usr/bin/python3
# murmur - timer module for controlling nodes/arms/actuators
# 1/16/18
# updated: 1/18/18

import logging
import logging.config
from datetime import datetime, timedelta


'''
1. start with M low; 2 second delay; repeat sequentially all the way to A
2. 20 second delay after low movement
3. start with A and fire both mid-ext and top; 5 second delay; repeat to L
'''

class Timer(object):
    arms = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M']

    pauses = {
        'low': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=10)
        },
        'mid': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=10)
        }
    }


    # def __init__(self):
    #     self.logger = self._initialize_logger()
    #
    # def _initialize_logger(self):
    #     logger = logging.getLogger('timer')
    #     logger.info('timer logger instantiated')
    #
    #     return logger

    def _get_pause(self, pause):
        return datetime.now() + pause

    def take_break(self, pause):
        pause = self._get_pause(pause)

        while True:
            if datetime.now() <= pause:
                yield None
            else:
                yield None
                break


    def fire_low(self):
        order = self.arms[::-1]  # start with arm M
        actuator = 'low'
        activate = True

        for arm in order:
            pause = self._get_pause(self.pauses['low']['sequence'])

            while True:
                if datetime.now() <= pause:
                    yield None
                else:
                    yield (arm, actuator, True)
                    break

    def fire_mid_and_top(self):
        order = self.arms
        actuators = ['mid-ext', 'top']
        activate = True

        for arm in order:
            pause = self._get_pause(self.pauses['mid']['sequence'])

            while True:
                if datetime.now() <= pause:
                    yield None
                else:
                    yield (arm, actuators[0], True)
                    yield (arm, actuators[1], True)
                    break

    def wrapper(self):
        print('firing low')
        for action in self.fire_low():
            yield action

        brk = self.pauses['low']['done']
        print('done firing low, taking a break for {} seconds...'.format(brk.seconds))
        for pause in self.take_break(brk):
            yield pause

        print('firing mid and top')
        for action in self.fire_mid_and_top():
            yield action

        brk = self.pauses['mid']['done']
        print('done firing mid-ext and top, taking a break for {} seconds...'.format(brk.seconds))
        for pause in self.take_break(brk):
            yield pause
