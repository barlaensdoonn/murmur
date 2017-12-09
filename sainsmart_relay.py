#!/usr/bin/python3
# murmur - sainsmart 4-channel relay board test
# 12/7/17
# updated: 12/9/17

'''
raspi connections to Sainsmart 4-channel 5V relay board:
    3.3V -> VCC
    5V -> JD-VCC
    GND -> GND
    GPIO -> IN*

power supply connections to relay terminals:
    +V power supply -> +V power input
    GND power supply -> NO relay terminal (far left when facing the relay terminals) -> GND power input
'''

import time
import gpiozero


class Relay(gpiozero.OutputDevice):
    '''
    class to extend gpiozero's OutputDevice base class

    OutputDevice has several useful methods including on(), off(), and toggle(),
    and some variables including pin, active_high, and initial_value.
    documentation here: https://gpiozero.readthedocs.io/en/stable/api_output.html#outputdevice
    '''

    def __init__(self, pin, *args, **kwargs):
        '''
        to use our own init in the Relay class, we must explicitly call
        the base class's __init__, otherwise it will be overridden
        more here: https://stackoverflow.com/questions/6396452/python-derived-class-and-base-class-attributes#6396839

        active_high=False initializes the relays on the Sainsmart board as off
        '''
        gpiozero.OutputDevice.__init__(self, pin, active_high=False, *args, **kwargs)

    def test_connection(self):
        '''
        test the pi's ability to control a relay
        do this BEFORE hooking up anything to the relay and watch LED on the relay board
        '''
        self.toggle()
        time.sleep(1)
        self.toggle()


if __name__ == '__main__':
    # list to store GPIO pins being used
    # find GPIO pin mappings here:
    # https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
    pins = [4, 5, 6, 13]
    relays = [Relay(pin) for pin in pins]  # list to hold initialized Relay objects

    # loop through the relays, turning them on for 1 second
    for relay in relays:
        relay.test_connection()
