#!/usr/bin/python3
# murmur - timer module for controlling nodes/arms/actuators
# 1/16/18
# updated: 6/18/18

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

    sequences = {
        'initialize': ['low', 'mid-retract_and_top', 'lowlow'],
        'main_loop': ['low', 'mid-ext_and_top', 'mid-retract_and_top', 'lowlow'],
        'shutdown': ['low', 'mid-ext_and_top', 'lowlow', 'release_mid-ext']
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


class Anchorage:
    '''
    '''

    all_arms_cw = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M']
    all_arms_ccw = ['M', 'L', 'K', 'J', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
    bottom_arms_cw = ['A', 'C', 'E', 'G', 'J', 'L']
    bottom_arms_ccw = ['L', 'J', 'G', 'E', 'C', 'A']
    top_arms_cw = ['B', 'D', 'H', 'K', 'F', 'M']  # NOTE: weird order so arms don't conflict
    top_arms_ccw = ['M', 'K', 'F', 'H', 'D', 'B']  # NOTE: this is a hack to get F out of the way of H on the mid movement

    # TODO: figure out initialize and shutdown sequences
    #
    # we could potentially delete the 'close' action from the end of 'initialize',
    # and just pause after 'initialize' finishes until blocks are removed. this
    # means the first loop would start from the open state, not dome state.
    # we could instead leave 'close' and pause after 'top_restore' to wait for
    # block removal. this means that 'top_restore' needs to make sure top lows are fired
    #
    # for shutdown we need to pause before 'release_top_lows' and 'release_all_mids'
    # to wait for block removal

    sequences = {
        'start': ['top_restore'],
        'initialize': ['bottom_restore', 'close'],
        'main_loop': ['open', 'bottom_collapse', 'top_collapse', 'top_restore', 'bottom_restore', 'close'],
        'shutdown': ['top_restore', 'bottom_restore', 'bottom_collapse', 'top_collapse'],
        'stop': ['release_top_lows', 'release_all_mids'],
    }

    actions = {
        'open': {
            'order': all_arms_cw,
            'actuators': ['low', 'mid-ext'],  # mid-ext is here to ensure it's fired when 'main_loop' is first run
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
            'actuators': ['low', 'mid-retract', 'mid-ext'],  # low is here to raise top lows during 'initialize' to allow for block removal
            'activate': [True, False, True]
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
        },
        'release_top_lows': {
            'order': top_arms_ccw,
            'actuators': ['low'],
            'activate': [False]
        },
        'release_all_mids': {
            'order': all_arms_ccw,
            'actuators': ['mid-retract'],
            'activate': [False]
        },
    }

    pauses = {
        'open': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=90)
        },
        'bottom_collapse': {
            'sequence': timedelta(seconds=8),
            'done': timedelta(seconds=45)
        },
        'top_collapse': {
            'sequence': timedelta(seconds=16),
            'done': timedelta(seconds=300)
        },
        'top_restore': {
            'sequence': timedelta(seconds=12),
            'done': timedelta(seconds=45)
        },
        'bottom_restore': {
            'sequence': timedelta(seconds=8),
            'done': timedelta(seconds=105)
        },
        'close': {
            'sequence': timedelta(seconds=2),
            'done': timedelta(seconds=600)
        },
        'release_top_lows': {
            'sequence': timedelta(seconds=4),
            'done': timedelta(seconds=45)
        },
        'release_all_mids': {
            'sequence': timedelta(seconds=1),
            'done': timedelta(seconds=2)
        }
    }


class Timer:
    '''
    machinery to (somewhat) asynchronously run the sequences specified by
    the timer class passed into __init__()
    '''

    def __init__(self, timer=None):
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
        we yield None if pause (a datetime.timedelta object) is in the future,
        otherwise we yield an action. we have to yield None to give the watchdog
        a chance to concurrently check for state changes while a sequence is running.
        also if the actuator is a 'mid' we pause 1/10th a second to ensure both
        mid-valves are never fired at the same time.
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

                        # slight pause to ensure both mid valves are never open simultaneously
                        if 'mid' in actuators[i]:
                            time.sleep(0.1)
                    break

    def run(self, sequence):
        seq = self.sequences[sequence]

        for thing in seq:
            yield from self._fire(thing)
            yield from self._pause(thing)
