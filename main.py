#!/usr/bin/python3
# murmur - main module
# 1/11/18
# updated: 1/11/18

import yaml
import socket
import logging
import logging.config


def _get_hostname():
    return socket.gethostname().split('.')[0]


def _get_logfile_name():
    '''format log file as "hostname.log"'''

    return '{dir}/{hostname}.log'.format(dir='logs', hostname=_get_hostname())


if __name__ == '__main__':
    with open('log.yaml', 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    log_config['handlers']['file']['filename'] = _get_logfile_name()
    logging.config.dictConfig(log_config)
    logging.info('* * * * * * * * * * * * * * * * * * * *')
    logging.info('logging configured')
