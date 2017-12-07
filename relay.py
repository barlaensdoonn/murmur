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


def initialize_pin(pin):
    '''active_high = False initializes Sainsmart 4-channel relay board as off'''

    return gpiozero.OutputDevice(pin, active_high = False)


if __name__ == '__main__':
    pins = [4, 5, 6]  # list to store GPIO pins being used
    relays = [initialize_pin(pin) for pin in pins]  # list to store initialized GPIO pins for controlling relays

    for relay in relays:
        relay.on()
        time.sleep(2)
        relay.off()
