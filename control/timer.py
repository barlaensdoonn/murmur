#!/usr/bin/python3
# murmur - timer module for controlling nodes/arms/actuators
# 1/16/18
# updated: 1/18/18

import logging
import logging.config
from datetime import datetime, timedelta


'''
start with M low; 2 second lag, move on to L all the way to A
20 second delay
start with A mid-ext
'''

class Timer(object):
    arms = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M']

    pauses = {
        'low': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=20)
        },
        'mid': {
            'between': timedelta(seconds=5),
            'after': timedelta(seconds=60)
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

    def take_break(self, pause):
        pause = self._get_pause(pause)

        while True:
            if datetime.now() <= pause:
                yield None
            else:
                yield None
                break


    def fire_low(self):
        order = arms[::-1]  # start with arm M
        actuator = 'low'
        activate = True

        for arm in order:
            pause = self._get_pause(pauses['low']['sequence'])

            while True:
                if datetime.now() <= pause:
                    yield None
                else:
                    yield (arm, actuator, True)
                    break

    def fire_mid_and_top(self):
        order = arms
        actuators = ['mid-ext', 'top']
        activate = True

        for arm in order:
            pause = self._get_pause(self.pauses['mid']['sequence'])

            while True: if datetime.now() <= pause:
                yield None
            else:
                yield (arm, actuators[0], True)
                yield (arm, actuators[1], True)
                break

    def wrapper(self):
        for action in fire_low():
            yield action

        print('done yielding, sleeping for 20 seconds'.format())
        yield take_break(self.pauses['low']['done'])

        for action in fire_mid_and_top(self):
            yield action

        print('done yielding, sleeping for 60 seconds...')
        yield take_break(self.pauses['mid']['done'])
