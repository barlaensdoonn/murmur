#!/usr/bin/python3
# murmur - manual control functions
# 6/18/18
# updated: 6/18/18

import time
from send import NodeMessage, Sender
sender = Sender('debug')

host_arm_map = {
    'murmur01': ['A', 'B', 'C'],
    'murmur02': ['D', 'E', 'F'],
    'murmur03': ['G', 'H', 'J'],
    'murmur04': ['K', 'L', 'M']
}


def get_host_by_arm(arm):
    for host in host_arm_map:
        if arm in host_arm_map[host]:
            return host


def fire(arms, action):
    '''
    arms can be a single arm or a list of arms.
    action should be tuple formatted as (actuator, activate).
    interestingly activate can be either True or 'true' since it gets dumped
    to json when NodeMessage is instantiated.
    '''
    arms = [arms] if type(arms) is not list else arms

    for arm in arms:
        msg = NodeMessage(arm, action[0], action[1])
        host = '{}.local'.format(get_host_by_arm(arm))
        sender.send_msg(host, msg.msg)


def _move_mids(arms, direction=None):
    if not direction or direction not in ['raise', 'drop']:
        print('please specify a valid direction')
        return

    actuators = ['mid-retract', 'mid-ext'] if direction is 'raise' else ['mid-ext', 'mid-retract']
    activate = [False, True]

    for arm in arms:
        for action in zip(actuators, activate):
            fire(arm, action)
            time.sleep(0.1)


def raise_mids(arms):
    _move_mids(arms, direction='raise')


def drop_mids(arms):
    _move_mids(arms, direction='drop')
