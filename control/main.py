#!/usr/bin/python3
# murmur - main module for nodes
# 1/16/18
# updated: 3/4/18

import os
import sys
import time
import yaml
import socket
import logging
import logging.config
from timer import Timer
from send import NodeMessage, Sender

host_arm_map = {
    'murmur01': ['A', 'B', 'C'],
    'murmur02': ['D', 'E', 'F'],
    'murmur03': ['G', 'H', 'J'],
    'murmur04': ['K', 'L', 'M']
}


def _get_logfile_name(basepath, hostname):
    '''format log file as "hostname.log"'''

    return os.path.join(basepath, '{hostname}.log'.format(hostname=hostname))


def _initialize_logger():
    logger = logging.getLogger('main')
    logger.info('main logger instantiated')

    return logger


def get_basepath():
    return os.path.dirname(os.path.realpath(__file__))


def get_hostname():
    return socket.gethostname().split('.')[0]


def get_host_by_arm(arm):
    for host in host_arm_map:
        if arm in host_arm_map[host]:
            return host


def configure_logger(basepath, hostname):
    with open(os.path.join(basepath, 'log.yaml'), 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    log_config['handlers']['file']['filename'] = _get_logfile_name(basepath, hostname)
    logging.config.dictConfig(log_config)
    logging.info('* * * * * * * * * * * * * * * * * * * *')
    logging.info('logging configured')

    return _initialize_logger()


def quit():
    logger.info('quitting program...')
    sys.exit()


def run_sequence(sequence):
    logger.info('running sequence {}'.format(sequence))

    try:
        for event in timer.run(sequence):
            if event:
                action = event
                host = '{}.local'.format(get_host_by_arm(action[0]))
                msg = NodeMessage(*action)
                sender.send_msg(host, msg.msg)

        logger.info('done running sequence {}'.format(sequence))
        return None
    except socket.gaierror:
        logger.error('unable to connect to host {}'.format(host))
        logger.error('sleeping for 1 minute, then trying again')
        time.sleep(60)
    except ConnectionRefusedError:
        logger.error('connection refused when trying to send message to host {}'.format(host))
        logger.error('{} possibly not running its main node program'.format(host))
        quit()
    except KeyboardInterrupt:
        logger.info('''...user exit received...''')
        quit()
    except Exception:
        logger.exception('unexpected exception!!')
        quit()


class State:

    state_file = 'state.txt'

    states = {
        'pause': None,
        'resume': 'continue',
        'start': ['initialize', 'main_loop'],
        'stop': 'shutdown'
    }

    def __init__(self, logger):
        self.logger = logger
        self.state = self._read_state_file()
        self.past_state = None

    def _read_state_file(self):
        with open(self.state_file, 'r') as fyle:
            return fyle.read().strip(' \n')

    def _register_state_change(self, current):
        self.past_state = self.state
        self.state = current

    def check_state(self):
        current = self._read_state_file()

        if current != self.state:
            self.logger('state change registered from {} to {}'.format(self.state, current))
            self._register_state_change(current)
            return self.state
        else:
            return None


if __name__ == '__main__':
    logger = configure_logger(get_basepath(), get_hostname())
    state = State(logger)
    sender = Sender(__name__)
    timer = Timer()
    initializing = True
    running = True

    while initializing:
        initializing = run_sequence('initialize')

    while running:
        run_sequence('main_loop')
