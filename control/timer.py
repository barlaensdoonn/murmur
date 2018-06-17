#!/usr/bin/python3
# murmur - timer module for controlling nodes/arms/actuators
# 1/16/18
# updated: 6/16/18

import time
import logging
from datetime import datetime, timedelta


class Mystic:
    '''
    1. activate M low; 2 second delay; repeat sequentially all the way to A
    2. 10 second delay after low movement
    3. start with A and simultaneously activate mid-ext and deactivate top; 5 second delay; repeat to M
    4. 2 minute rest in fully open position
    5. activate M top, deactivate mid-ext, 0.1 second delay, activate mid-retract; repeat to A
    6. 1 minute pause
    7. deactivate low A; 2 second pause; repeat to M
    8. 3 minute rest in fully closed position
    9. repeat #1 - #8
    '''
    arms_A_to_M = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M']
    arms_M_to_A = ['M', 'L', 'K', 'J', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

    pauses = {
        'low': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=10)
        },
        'mid-ext_and_top': {
            'sequence': timedelta(seconds=5),
            'done': timedelta(seconds=120)
        },
        'mid-retract_and_top': {
            'sequence': timedelta(seconds=5),
            'done': timedelta(seconds=60)
        },
        'lowlow': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=180)
        },
        'release_mid-ext': {
            'sequence': timedelta(seconds=1),
            'done': timedelta(seconds=60)
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
            'actuators': ['mid-retract', 'mid-ext', 'top'],
            'activate': [False, True, False]
        },
        'mid-retract_and_top': {
            'order': arms_M_to_A,
            'actuators': ['top', 'mid-ext', 'mid-retract'],
            'activate': [True, False, True]
        },
        'lowlow': {
            'order': arms_M_to_A,
            'actuators': ['low'],
            'activate': [False]
        },
        'release_mid-ext': {
            'order': arms_M_to_A,
            'actuators': ['mid-ext'],
            'activate': [False]
        }
    }

    sequences = {
        'initialize': ['low', 'mid-retract_and_top', 'lowlow'],
        'main_loop': ['low', 'mid-ext_and_top', 'mid-retract_and_top', 'lowlow'],
        'shutdown': ['low', 'mid-ext_and_top', 'lowlow', 'release_mid-ext']
    }


class Anchorage:
    '''
    '''

    all_arms_cw = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M']
    all_arms_ccw = ['M', 'L', 'K', 'J', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
    bottom_arms_cw = ['A', 'C', 'E', 'G', 'J', 'L']
    bottom_arms_ccw = ['L', 'J', 'G', 'E', 'C', 'A']
    top_arms_cw = ['B', 'D', 'F', 'H', 'K', 'M']
    top_arms_ccw = ['M', 'K', 'F', 'H', 'D', 'B']  # NOTE: this is a hack to get F out of the way of H on the mid movement

    pauses = {
        'open': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=30)
        },
        'bottom_collapse': {
            'sequence': timedelta(seconds=4),
            'done': timedelta(seconds=45)
        },
        'top_collapse': {
            'sequence': timedelta(seconds=12),
            'done': timedelta(seconds=300)
        },
        'top_restore': {
            'sequence': timedelta(seconds=8),
            'done': timedelta(seconds=45)
        },
        'bottom_restore': {
            'sequence': timedelta(seconds=4),
            'done': timedelta(seconds=75)
        },
        'close': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=600)
        }
    }

    actions = {
        'open': {
            'order': all_arms_cw,
            'actuators': ['low', 'mid-ext'],  # mid-ext is here to ensure it's fired when the pingo first starts up
            'activate': [True, True]
        },
        'bottom_collapse': {
            'order': bottom_arms_cw,
            'actuators': ['low', 'mid-ext', 'mid-retract', 'top'],
            'activate': [False, False, True, True]
        },
        'top_collapse': {
            'order': top_arms_cw,
            'actuators': ['mid-ext', 'mid-retract'],
            'activate': [False, True]
        },
        'top_restore': {
            'order': top_arms_ccw,
            'actuators': ['mid-retract', 'mid-ext'],
            'activate': [False, True]
        },
        'bottom_restore': {
            'order': bottom_arms_ccw,
            'actuators': ['top', 'mid-retract', 'mid-ext', 'low'],
            'activate': [False, False, True, True]
        },
        'close': {
            'order': all_arms_ccw,
            'actuators': ['low'],
            'activate': [False]
        }
    }

    # TODO: figure out initialize and shutdown sequences
    sequences = {
        'initialize': ['open', 'bottom_collapse', 'top_collapse', 'top_restore', 'bottom_restore', 'close'],
        'main_loop': ['open', 'bottom_collapse', 'top_collapse', 'top_restore', 'bottom_restore', 'close'],
        # 'shutdown': ['low', 'mid-ext_and_top', 'lowlow', 'release_mid-ext']
    }


class Timer:
    '''
    machinery to (somewhat) asynchronously run the sequences specified by
    the timer class passed into __init__()
    '''

    def __init__(self, timer):
        self.logger = self._initialize_logger()
        self.pauses = timer.pauses
        self.actions = timer.actions
        self.sequences = timer.sequences

    def _initialize_logger(self):
        logger = logging.getLogger('timer')
        logger.info('timer logger instantiated')

        return logger

    def _get_pause(self, pause):
        return datetime.now() + pause

    def _pause(self, action):
        paws = self.pauses[action]['done']
        self.logger.info('done firing {action}, pausing for {pause} seconds...'.format(action=action, pause=paws.seconds))
        pause = self._get_pause(paws)

        while True:
            if datetime.now() <= pause:
                yield None
            else:
                yield None
                break

    def _fire(self, action):
        '''
        we pause slightly to ensure both mid-valves are never fired at the same time.
        the pause is located at the NOTE below.
        '''
        self.logger.info('firing {}'.format(action))

        for arm in self.actions[action]['order']:
            pause = self._get_pause(self.pauses[action]['sequence'])

            while True:
                if datetime.now() <= pause:
                    yield None
                else:
                    actuators = self.actions[action]['actuators']
                    activate = self.actions[action]['activate']

                    for i in range(len(actuators)):
                        action_tuple = (arm, actuators[i], activate[i])
                        self.logger.debug('yielding action: {}'.format(action_tuple))
                        yield (action_tuple)

                        # NOTE: slight pause to ensure both mid valves are never open simultaneously
                        if 'mid' in actuators[i]:
                            time.sleep(0.1)
                    break

    def run(self, sequence):
        seq = self.sequences[sequence]

        for thing in seq:
            yield from self._fire(thing)
            yield from self._pause(thing)
