#!/usr/bin/env python3

import queue
import signal
import sys
import RPi.GPIO as GPIO

BUTTON_GPIO = 16
LED_GPIO = 20

# The callback only reports what happened; the main loop decides what to do
button_events = queue.Queue()

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_released_callback(channel):
    button_events.put("released")

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_GPIO, GPIO.OUT)

GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback=button_released_callback, bouncetime=200)

signal.signal(signal.SIGINT, signal_handler)

blinking = False
led_on = False

while True:
    try:
        # Wait up to half a second for a button event: this wait is also the blink timing
        button_events.get(timeout=0.5)
        blinking = not blinking
        if not blinking:
            led_on = False                  # blinking stopped: the LED must not stay on
    except queue.Empty:
        if blinking:
            led_on = not led_on             # no button event: next step of the blinking
    GPIO.output(LED_GPIO, led_on)
