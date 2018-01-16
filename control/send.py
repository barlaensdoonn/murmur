#!/usr/bin/python3
# murmur - send socket messages for controlling nodes
# 1/12/18
# updated: 1/16/18

import json
import socket

'''
messages are sent to specific hosts
message format:

msg = {
    'arm': 'A',
    'actuator': 'low',
    'activate': True
}
'''

class Send(object):

    def __init__(self):
        self.logger = _initialize_logger()

    def _initialize_logger(self):
        logger = logging.getLogger('send')
        logger.info('node logger instantiated')

        return logger

    def _encode_msg(self, msg):
        return '{}\r\n'.format(msg).encode()

    def package_msg(self, arm, actuator, activate):
        msg = {
            'arm': arm,
            'actuator': actuator,
            'activate': activate
        }

        return json.dumps(msg)

    def context_tcp(self, host, msg):
        '''
        hostport in client connect should be tuple (host, port)
        '''

        hostport = (host, 9999)
        encoded = _encode_msg(msg)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect(hostport)
            self.logger.info('sending message "{msg}" to host {host} on port {port}'.format(msg=msg, host=host, port=port))
            client.sendall(encoded)

            data = client.recv(1024)
            print('received: {}'.format(data.decode()))
            self.logger.info('received message "{data}"'.format(data=data))
