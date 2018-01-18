#!/usr/bin/python3
# murmur - timer module for controlling nodes/arms/actuators
# 1/16/18
# updated: 1/18/18

import time
import logging
import logging.config
from datetime import datetime, timedelta


'''
1. start with M low; 2 second delay; repeat sequentially all the way to A
2. 20 second delay after low movement
3. start with A and fire both mid-ext and top; 5 second delay; repeat to L
4. reverse starting with M top and mid-retract; then low
'''

class Timer(object):
    arms_A_to_M = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M']
    arms_M_to_A = ['M', 'L', 'K', 'J', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

    pauses = {
        'low': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=10)
        },
        'mid-ext_and_top': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=10)
        },
        'mid-retract_and_top': {
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
        },
        'mid-retract_and_top': {
            'order': arms_M_to_A,
            'actuators': ['top', 'mid-ext', 'mid-retract'],
            'activate': [False, False, True]
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

    def _take_break(self, pause):
        print('done firing low, taking a break for {} seconds...'.format(pause.seconds))
        pause = self._get_pause(pause)

        while True:
            if datetime.now() <= pause:
                yield None
            else:
                yield None
                break

    def _fire(self, action):
        print('firing {}'.format(action))
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
                        if actuators[i] == 'mid-ext':
                            time.sleep(0.1)
                    break

    def wrapper(self):
        for action in self._fire('low'):
            yield action

        for pause in self._take_break(self.pauses['low']['done']):
            yield pause

        for action in self._fire('mid-ext_and_top'):
            yield action

        for pause in self._take_break(self.pauses['mid-ext_and_top']['done']):
            yield pause
