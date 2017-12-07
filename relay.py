#!/usr/bin/python3
# murmur
# 11/27/17
# updated: 12/7/17

'''
raspi connections to Sainsmart 4-channel 5V relay board:
    3.3V -> VCC
    5V -> JD-VCC
    GND -> GND
    GPIO -> IN*

power supply connections to relay terminals:
    +V power supply -> +V power input
    GND power supply -> NO relay terminal -> GND power input
'''

import time
import gpiozero


def _initialize_pin(pin):
    '''active_high = False initializes Sainsmart 4-channel relay board as off'''

    return gpiozero.OutputDevice(pin, active_high=False)


def initialize_relays(pins):
    '''returns list of gpiozero.OutputDevice objects'''

    return [_initialize_pin(pin) for pin in pins]


if __name__ == '__main__':
    pins = [4, 5, 6]  # GPIO pins being used
    relays = intialize_relays(pins)

    for relay in relays:
        relay.on()
        time.sleep(1)
        relay.off()
