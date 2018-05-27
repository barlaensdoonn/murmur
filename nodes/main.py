#!/usr/bin/python3
# murmur - main module for nodes
# 1/11/18
# updated: 1/23/18

import os
import yaml
import socket
import logging
import logging.config
from node import Node
from receive import Receive


basepath = '/home/pi/gitbucket/murmur/nodes'


def _get_logfile_name(hostname):
    '''format log file as "hostname.log"'''

    return os.path.join(basepath, '{hostname}.log'.format(hostname=hostname))


def _initialize_logger():
    logger = logging.getLogger('main')
    logger.info('main logger instantiated')

    return logger


def get_hostname():
    return socket.gethostname().split('.')[0]


def configure_logger(hostname):
    with open(os.path.join(basepath, 'log.yaml'), 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    log_config['handlers']['file']['filename'] = _get_logfile_name(hostname)
    logging.config.dictConfig(log_config)
    logging.info('* * * * * * * * * * * * * * * * * * * *')
    logging.info('logging configured')

    return _initialize_logger()


def initialize_node(hostname):
    logger.info('...initializing node...')

    return Node(hostname)


def initialize_receive(node):
    logger.info('...initializing receive...')

    return Receive(node)


if __name__ == '__main__':
    hostname = get_hostname()
    logger = configure_logger(hostname)
    node = initialize_node(hostname)
    receive = initialize_receive(node)

    try:
        logger.info('receive server entering serve_forever() loop')
        receive.server.serve_forever()
    except KeyboardInterrupt:
        receive.server.shutdown()
        logger.info('...user exit received, shutting down server...')
