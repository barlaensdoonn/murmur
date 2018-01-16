#!/usr/bin/python3
# murmur - communicate between nodes
# 1/12/18
# updated: 1/12/18

import socket
from curio import run, tcp_server


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


async def echo_client(client, addr):
    print('Connection from', addr)

    while True:
        data = await client.recv(1000)
        if not data:
            break
        await client.sendall(data)

    print('Connection closed')


if __name__ == '__main__':
    try:
        run(tcp_server, '', 25000, echo_client)
    except KeyboardInterrupt:
        print('terminating server')
