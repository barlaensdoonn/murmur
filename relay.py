#!/usr/bin/python3
# murmur
# 11/27/17
# updated: 11/27/17

import time
import gpiozero

relay_pin = 4
relay = gpiozero.OutputDevice(relay_pin, active_high=False)  # active_high = False for Sainsmart 4-channel relay board

relay.on()
time.sleep(2)
relay.off()
