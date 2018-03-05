#!/usr/bin/python3
# murmur - watchdog to monitor state changes registered by touchscreen buttons
# 3/1/18
# updated: 3/4/18

import time
import logging


class Watchdog:

    state_file = 'state.txt'

    state_map = {
        'start': ['initialize', 'main_loop'],
        'stop': ['shutdown']
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
        self.state = current

    def _pause(self):
        self.logger.info('pausing program...')

        while True:
            if self.check_state():
                break
            else:
                time.sleep(0.1)

    def _handle_state_change(self, current):
        self._register_state_change(current)

        if self.state == 'pause':
            self._pause()
        elif self.state == 'resume':
            self.logger.info('resuming regularly scheduled programming')
        else:
            pass

    def check_state(self):
        current = self._read_state_file()

        if current and current != self.state:
            self.logger.info('state change registered from {} to {}'.format(self.state.upper(), current.upper()))
            self._handle_state_change(current)
            return self.state
        else:
            return None
