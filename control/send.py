#!/usr/bin/python3
# murmur - send socket messages for controlling nodes
# 1/12/18
# updated: 6/17/18

import json
import socket
import logging


class NodeMessage(object):
    '''
    instruction for node to carry out some action.

    format:
    msg = {
        'arm': 'A',
        'actuator': 'low',
        'activate': True
    }
    '''

    def __init__(self, arm, actuator, activate):
        self.arm = arm
        self.actuator = actuator
        self.activate = activate
        self.msg = self._package_msg()

    def _package_msg(self):
        msg = {
            'arm': self.arm,
            'actuator': self.actuator,
            'activate': self.activate
        }

        return json.dumps(msg)


class Sender(object):
    '''class to handle sending client socket messages to listening servers'''

    def __init__(self, calling_module):
        self.calling_module = calling_module
        self.logger = self._initialize_logger()

    def _initialize_logger(self):
        logger = logging.getLogger('send')
        logger.info('send logger instantiated from {}'.format(self.calling_module))

        return logger

    def _encode_msg(self, msg):
        return '{}\r\n'.format(msg).encode()

    def _tcp_client_send(self, host, msg):
        '''hostport in client.connect() should be a tuple formatted (host, port)'''
        hostport = (host, 9999)
        encoded = self._encode_msg(msg)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(hostport)
            client.sendall(encoded)

            data = client.recv(1024)

            if data == encoded:
                self.logger.info('host {host} acknowledged message was received'.format(host=host))

    def send_msg(self, host, msg):
        self.logger.info('sending message "{msg}" to host {host}'.format(msg=msg, host=host))
        self._tcp_client_send(host, msg)
