#!/usr/bin/python3
# murmur - communicate between nodes
# 1/12/18
# updated: 1/12/18

import socket


def _encode_msg(msg):
    return '{}\r\n'.format(msg).encode()


def context_tcp(hostport, msg):
    '''
    use something like this to send messages to the server
    hostport should be tuple (host, port)
    '''

    msg = _encode_msg(msg)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(hostport)
        client.sendall(msg)
        data = client.recv(1024)
        print('received: {}'.format(data.decode()))
