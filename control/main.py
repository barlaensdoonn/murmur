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
from watchdog import Watchdog

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


def run_sequence(watchdog, sequence):
    logger.info('running sequence {}'.format(sequence))

    try:
        for event in timer.run(sequence):

            # if the state is updated and it's one we're interested in (either 'start' or 'stop'),
            # and the current sequence is not in the new state's sequences list,
            # stop current sequence by returning the sequence(s) to be run next
            if watchdog.check_state() and watchdog.state in watchdog.state_map.keys():
                if sequence not in watchdog.state_map[watchdog.state]:
                    print('returning {}'.format(watchdog.state_map[watchdog.state]))
                    return watchdog.state_map[watchdog.state]

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


def run(watchdog):
    '''
    when first launched the run loop should wait for a 'start' or 'stop' signal before doing anything.
    on 'start' we should run 'initialize' sequence, then run 'main_loop' indefinitely until 'stop' is received,
    at which point it should run the 'shutdown' sequence.
    'pause' and 'resume' are currently handled within the Watchdog class
    '''

    while watchdog.check_state() not in watchdog.state_map.keys():
        time.sleep(0.1)


if __name__ == '__main__':
    logger = configure_logger(get_basepath(), get_hostname())
    watchdog = Watchdog()
    sender = Sender(__name__)
    timer = Timer()
    initializing = True
    running = True

    run(watchdog)

    while initializing:
        initializing = run_sequence(watchdog, 'initialize')

    while running:
        run_sequence(watchdog, 'main_loop')
