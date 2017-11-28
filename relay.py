#!/usr/bin/python3
# murmur
# 11/27/17
# updated: 11/27/17

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


def initialize_relay():
    relay_pin = 4
    # active_high = False to initialize Sainsmart 4-channel relay board as off
    relay = gpiozero.OutputDevice(relay_pin, active_high = False)

    return relay


def on():
    relay.on()


def off():
    relay.off()


if __name__ == '__main__':
    relay = initialize_relay()

    relay.on()
    time.sleep(2)
    relay.off()
