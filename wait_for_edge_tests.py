#!/usr/bin/python3

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Function that will be called when rising (from 0 to 1) event is detected
def my_callback_rising():
    print('Uy kieto, rising edge')

# Function that will be called when rising (from 1 to 0) event is detected
def my_callback_falling():
    print('Uy kieto, falling edge')

# Setting up the GPIO23 pin as input with pull_down logic (default 0 state when connected to GND)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.add_event_detect(23, GPIO.RISING, callback=my_callback_rising)
# GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback_falling)

try:  
    print("Waiting for falling edge on port 23")
    GPIO.wait_for_edge(23, GPIO.RISING)
    print("Rising edge detected.")
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit