#!/usr/bin/python3
# murmur - single relay class
# 12/7/17
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


class Relay(object):

    def __init__(self, pin):
        self.pin = pin
        self.relay = self._initialize_relay()

    def _initialize_relay(self):
        '''active_high = False initializes Sainsmart 4-channel relay board as off'''

        return gpiozero.OutputDevice(self.pin, active_high=False)

    def test_connection(self):
        self.relay.toggle()
        time.sleep(1)
        self.relay.toggle()


if __name__ == '__main__':
    pin = 4
    relay = Relay(pin)
    relay.test_connection()
