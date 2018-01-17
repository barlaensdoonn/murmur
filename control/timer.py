#!/usr/bin/python3
# murmur - timer module for controlling nodes/arms/actuators
# 1/16/18
# updated: 1/16/18

import logging
import logging.config


def initialize_logger():
    logger = logging.getLogger('timer')
    logger.info('timer logger instantiated')

    return logger


if __name__ == '__main__':
    logger = initialize_logger(hostname)
