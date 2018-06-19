#!/usr/bin/python3
# murmur - main control module
# 1/16/18
# updated: 6/19/18

'''
buttons.py and this main.py run concurrently as separate systemd services:
murmur_buttons.service
murmur_control.service

- - - - - - - - - - - - -

there are 4 modules that work together to construct the sequence to run:
- buttons.py writes the text of the button that is pressed (for example 'start'
  for the START button) to state.txt. when first launched buttons.py writes 'pause'
  and then waits for input from the touchscreen.
- watchdog.py monitors state.txt to check for changes in state. when a state change
  is registered, it translates that state into a sequence list by referencing its
  state_map class variable. this sequence list is returned and executed by run()
  and run_sequence() in this module.
- timer.py describes and stores the actual sequences and their relative actions,
  execution order, pauses, etc. it also contains the infrastructure to (relatively)
  asynchronously execute an action and pause in between actions.
- control/main.py (this module) uses run() and run_sequence() to get the current
  sequence to run from the watchdog. if the watchdog registers a new sequence
  that is not the currently running sequence, we break out of the current sequence
  and start executing the new one. run_sequence() actually loops over the generator
  function timer.run() to get events and then sends them to the listening nodes.
'''


import os
import sys
import time
import yaml
import socket
import logging
import logging.config
from timer import Anchorage, Timer
from send import NodeMessage, Sender
from watchdog import Watchdog


host_arm_map = {
    'murmur01': ['A', 'B', 'C'],
    'murmur02': ['D', 'E', 'F'],
    'murmur03': ['G', 'H', 'J'],
    'murmur04': ['K', 'L', 'M']
}


def _get_logfile_name(basepath, hostname):
    '''format log file as "hostname.log"'''
    return os.path.join(basepath, '{}.log'.format(hostname))


def _initialize_logger():
    logger = logging.getLogger('main')
    logger.info('main logger instantiated')

    return logger


def get_basepath(current_path=None):
    '''we need to pass in a path if not running this as a file'''
    path = __file__ if not current_path else current_path
    return os.path.dirname(os.path.realpath(path))


def get_hostname():
    return socket.gethostname().split('.')[0]


def get_host_by_arm(arm):
    for host in host_arm_map:
        if arm in host_arm_map[host]:
            return host


def configure_logger(basepath, hostname):
    with open(os.path.join(basepath, 'log.yaml'), 'r') as log_conf:
        log_config = yaml.safe_load(log_conf)

    log_config['handlers']['file']['filename'] = _get_logfile_name(basepath, hostname)
    logging.config.dictConfig(log_config)
    logging.info('* * * * * * * * * * * * * * * * * * * *')
    logging.info('logging configured')

    return _initialize_logger()


def quit():
    logger.info('quitting program...')
    sys.exit()


def sleep():
    logger.warning('sleeping for 10 seconds, then trying again')
    time.sleep(10)


def run_sequence(watchdog, sequence_list):
    '''
    we use the Watchdog class variable state_maps to break out of the loop
    if necessary: if the state is updated and it's one we're interested in
    (either 'start' or 'stop'), and the current sequence is not in the new state's
    sequence list in watchdog.state_maps, stop current sequence by returning the
    sequence list to be run next.

    since 'pause' is not in watchdog's state_maps, during 'pause' state we just
    run watchdog.check_state() until it returns 'start' or 'stop'.

    once the end of the timer.run(sequence) generator object is reached, we return
    the sequence we just ran if it was 'main_loop', otherwise we return None.
    refer to the NOTE below to see how we achieve this after running 'initialize'.
    '''

    # NOTE: we pop 'initialize' off front of copied list so we don't run it again
    # until next time CONFIRM BLOCKS OUT button is pressed. this works because only
    # 'confirm_blocks_out' sequence list has more than one element in it.
    safe_list = sequence_list[:]
    sequence = safe_list.pop(0) if len(safe_list) > 1 else safe_list[0]

    try:
        logger.info("running sequence '{}'".format(sequence))
        for event in timer.run(sequence):

            # refer to docstring for explanation of this block
            if watchdog.check_state() and watchdog.state in watchdog.state_map.keys():
                if sequence not in watchdog.state_map[watchdog.state]:
                    logger.info("breaking out of sequence '{}'".format(sequence))
                    return watchdog.state_map[watchdog.state]

            if event:
                action = event
                host = '{}.local'.format(get_host_by_arm(action[0]))
                msg = NodeMessage(*action)
                sender.send_msg(host, msg.msg)

        logger.info("done running sequence '{}'".format(sequence))
        return safe_list if 'main_loop' in safe_list else None

    except socket.gaierror:
        logger.error('unable to connect to host {}'.format(host))
        sleep()
    except ConnectionRefusedError:
        logger.error('connection refused when trying to send message to host {}'.format(host))
        logger.error('{} is down or possibly not running its main node program'.format(host))
        sleep()


def run(watchdog):
    '''
    at the top of the loop we wait for a 'start' or 'stop' signal before doing anything.
    on 'start' we run 'initialize' sequence, then run 'main_loop' indefinitely
    until 'stop' is received, at which point we run the 'shutdown' sequence.

    the Watchdog class has a class variable 'state_maps' that maps the states
    'start' and 'stop' to sequence lists, which are passed to run_sequence
    from here. 'state_maps' is also used in run_sequence to break out of the
    currently running sequence if a state change of 'start' or 'stop' is registered
    '''

    while True:
        try:
            # pause at the top of the loop since watchdog._pause() will only run when
            # a state change is registered, and the program starts in state 'pause'
            logger.info('waiting for input from touchscreen...')
            while watchdog.check_state() not in watchdog.state_map.keys():
                time.sleep(0.1)

            running = watchdog.state_map[watchdog.state]

            while running:
                running = run_sequence(watchdog, running)
        except KeyboardInterrupt:
            logger.info('''...user exit received...''')
            quit()
        except Exception:
            logger.exception('unexpected exception!!')
            quit()


if __name__ == '__main__':
    logger = configure_logger(get_basepath(current_path=None), get_hostname())
    watchdog = Watchdog()
    sender = Sender(__name__)
    anchor = Anchorage()
    timer = Timer(timer=anchor)

    run(watchdog)
