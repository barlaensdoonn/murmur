#!/usr/bin/python3
# murmur - main module for nodes
# 1/16/18
# updated: 2/19/18

import os
import sys
import time
import yaml
import socket
import logging
import logging.config
from timer import Timer
from send import NodeMessage, Sender


basepath = '/home/pi/gitbucket/murmur/control'

host_arm_map = {
    'murmur01': ['A', 'B', 'C'],
    'murmur02': ['D', 'E', 'F'],
    'murmur03': ['G', 'H', 'J'],
    'murmur04': ['K', 'L', 'M']
}


def _get_logfile_name(hostname):
    '''format log file as "hostname.log"'''

    return os.path.join(basepath, '{hostname}.log'.format(hostname=hostname))


def _initialize_logger():
    logger = logging.getLogger('main')
    logger.info('main logger instantiated')

    return logger


def get_hostname():
    return socket.gethostname().split('.')[0]


def get_host_by_arm(arm):
    for host in host_arm_map:
        if arm in host_arm_map[host]:
            return host


def configure_logger(hostname):
    with open(os.path.join(basepath, 'log.yaml'), 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    log_config['handlers']['file']['filename'] = _get_logfile_name(hostname)
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
    except KeyboardInterrupt:
        logger.info('''...user exit received...''')
        quit()
    except Exception:
        logger.exception('exception!!')
        logger.error('encountered error, shutting down')
        sys.exit()


if __name__ == '__main__':
    hostname = get_hostname()
    logger = configure_logger(hostname)
    sender = Sender(__name__)
    timer = Timer()
    initializing = True
    running = True

    while initializing:
        initializing = run_sequence('initialize')

    while running:
        run_sequence('main_loop')
