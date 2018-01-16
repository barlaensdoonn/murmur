#!/usr/bin/python3
# murmur - socket server for receiving network messages
# 11/24/17
# updated: 1/16/18

import yaml
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

        data = self.request.recv(1024)
        self.decoded = data.decode().strip()
        
        self.server.logger.info("{} wrote: {}".format(self.client_address[0], self.decoded))

        try:
            return {'host': msg[0], 'track': msg[1], 'volume': float(msg[2])}
        except IndexError:
            return None

    def handle(self):
        self.server.logger.debug('client {} connected'.format(self.client_address[0]))
        msg = self.parse_msg()

        if msg and msg['track'] in self.server.bmbx.sounds.keys():
            if msg['host'] == self.server.hostname:
                self.server.logger.info('asking boombox to play "{}" at volume {}'.format(msg['track'], msg['volume']))
                self.server.bmbx.play(msg['track'], msg['volume'])
            else:
                self.server.logger.info('received valid command {}, but not addressed to me, ignoring...'.format(self.decoded))
        else:
            self.server.logger.warning("invalid command '{}' received, ignoring...".format(self.decoded))

    def finish(self):
        '''finish method is always called by the base handler after handle method has completed'''

        self.server.logger.debug('closed connection from {}'.format(self.client_address[0]))


class Receive(object):

        def __init__(self):
            self.logger = self._initialize_logger()
            self.server = self._initialize_server()

        def _initialize_logger(self):
            logger = logging.getLogger('receive')
            logger.info('arm {} logger instantiated'.format('receive'))

            return logger

        def _initialize_server(self):
            hostport = ('', 9999)  # '' stands for all available interfaces
            hostname = socket.gethostname()
            self.logger.info('host {hostname} initializing open TCP server on port {port}'.format(hostname=hostname, port=hostport[1]))

            server = socketserver.TCPServer(hostport, TCPHandler)
            server.logger = self.logger
            server.hostname = hostname
