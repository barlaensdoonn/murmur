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
4. reverse starting with M top and mid-retract
'''

class Timer(object):
    arms_A_to_M = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M']
    arms_M_to_A = arms_A_to_M[::-1]

    pauses = {
        'low': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=10)
        },
        'mid-ext_and_top': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=10)
        }
    }

    actions = {
        'low': {
            'order': arms_M_to_A,
            'actuators': ['low'],
            'activate': [True]
        },
        'mid-ext_and_top': {
            'order': arms_A_to_M,
            'actuators': ['mid-ext', 'top'],
            'activate': [True, True]
        }
    }


    def __init__(self):
        self.logger = self._initialize_logger()

    def _initialize_logger(self):
        logger = logging.getLogger('timer')
        logger.info('timer logger instantiated')

        return logger

    def _get_pause(self, pause):
        return datetime.now() + pause

    def _take_break(self, pause):
        pause = self._get_pause(pause)

        while True:
            if datetime.now() <= pause:
                yield None
            else:
                yield None
                break

    def _fire(self, action):
        for arm in self.actions[action]['order']:
            pause = self._get_pause(self.pauses[action]['sequence'])

            while True:
                if datetime.now() <= pause:
                    yield None
                else:
                    actuators = self.actions[action]['actuators']
                    activate = self.actions[action]['activate']
                    for i in range(len(actuators)):
                        yield (arm, actuators[i], activate[i])
                    break

    def wrapper(self):
        print('firing low')
        for action in self._fire('low'):
            yield action

        brk = self.pauses['low']['done']
        print('done firing low, taking a break for {} seconds...'.format(brk.seconds))
        for pause in self._take_break(brk):
            yield pause

        print('firing mid and top')
        for action in self._fire('mid-ext_and_top'):
            yield action

        brk = self.pauses['mid-ext_and_top']['done']
        print('done firing mid-ext and top, taking a break for {} seconds...'.format(brk.seconds))
        for pause in self._take_break(brk):
            yield pause
