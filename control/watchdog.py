#!/usr/bin/python3
# murmur - watchdog to monitor state changes registered by touchscreen buttons
# 3/1/18
# updated: 6/18/18

import os
import time
import logging


def get_basepath():
    return os.path.dirname(os.path.realpath(__file__))


class Watchdog:
    '''
    state_file is the file updated by buttons.py when touchscreen buttons are pressed.
    state_map translates states to sequence lists for run and run_sequence in main.py
    '''

    state_file = os.path.join(get_basepath(), 'state.txt')

    state_map = {
        'start': ['start'],
        'confirm blocks out': ['initialize', 'main_loop'],
        'shutdown': ['shutdown'],
        'confirm blocks in': ['stop']
    }

    def __init__(self):
        self.logger = self._initialize_logger()
        self.state = self._read_state_file()
        self.logger.info('watchdog initialized with state {}'.format(self.state.upper()))

    def _initialize_logger(self):
        logger = logging.getLogger('watchdog')
        logger.info('watchdog logger instantiated')

        return logger

    def _read_state_file(self):
        with open(self.state_file, 'r') as fyle:
            return fyle.read().strip(' \n')

    def _register_state_change(self, current):
        self.logger.info('state change registered from {} to {}'.format(self.state.upper(), current.upper()))
        self.state = current

    def _pause(self):
        '''sleep and wait for check_state() method to return a new state'''
        self.logger.info('pausing program...')

        while True:
            if self.check_state():
                break
            else:
                time.sleep(0.1)

    def _handle_state_change(self, current):
        '''this method is used to pause the program if 'pause' state is registered'''
        self._register_state_change(current)

        if self.state == 'pause':
            self._pause()
        elif self.state == 'resume':
            self.logger.info('resuming regularly scheduled programming')
        else:
            pass

    def check_state(self):
        '''
        if there is a state change, return the state, otherwise return None.
        _pause() method in particular uses this to break out of sleep loop if
        something other than None is returned.
        '''
        current = self._read_state_file()

        if current and current != self.state:
            self._handle_state_change(current)
            return self.state
        else:
            return None
