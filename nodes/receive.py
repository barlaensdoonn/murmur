#!/usr/bin/python3
# murmur - socket server for receiving network messages
# 11/24/17
# updated: 1/16/18

import yaml
import json
import socket
import logging
import socketserver


class TCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the client.
    """

    def parse_msg(self):
        '''self.request is the TCP socket connected to the client'''

        # receive data
        data = self.request.recv(1024)
        self.decoded = data.decode().strip()
        self.server.logger.info('{} wrote: {}'.format(self.client_address[0], self.decoded))

        # acknowledge message was received by sending it back
        self.server.logger.info('sending acknowledgement back to client')
        self.request.sendall(data)

        # message should be in json format
        try:
            return json.loads(self.decoded)
        except Exception:
            self.server.logger.error('exception!!')

    def handle(self):
        self.server.logger.debug('client {} connected'.format(self.client_address[0]))
        action = self.parse_msg()
        self.node.parse_action(action)

    def finish(self):
        '''finish method is always called by the base handler after handle method has completed'''

        self.server.logger.debug('closing connection from {}'.format(self.client_address[0]))


class Receive(object):

        def __init__(self, node):
            self.logger = self._initialize_logger()
            self.server = self._initialize_server()
            self.node = node

        def _initialize_logger(self):
            logger = logging.getLogger('receive')
            logger.info('receive logger instantiated')

            return logger

        def _initialize_server(self):
            hostport = ('', 9999)  # '' stands for all available interfaces
            hostname = socket.gethostname()
            self.logger.info('host {hostname} initializing open TCP server on port {port}'.format(hostname=hostname, port=hostport[1]))

            server = socketserver.TCPServer(hostport, TCPHandler)
            server.logger = self.logger
            server.hostname = hostname
            server.node = self.node

            return server
