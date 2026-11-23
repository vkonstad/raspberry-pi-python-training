# Example Hardware 07 - Input and Output Threads
# One input and two outputs, each handled by its own thread:
#   - the button thread watches the button (input)
#   - the blink thread blinks LED 1 on and off (digital output)
#   - the fade thread makes LED 2 slowly brighten and dim (PWM output)
# Each button press switches both LEDs on or off. The main thread only keeps the program alive.
# Wiring: button on BUTTON_GPIO (pull-up), LED 1 on LED_GPIO, LED 2 on PWM_LED_GPIO
# (each LED with a resistor). The button and LED 1 are the same as in Example Hardware 04-06.
# Stop with Ctrl+C.
#
# Concepts: threading (Example 08), threading.Event for communication and stopping,
#           PWM (Example Hardware 02), logging with the thread name, polling an input,
#           GPIO cleanup in finally

import logging
import threading
import time
import RPi.GPIO as GPIO

BUTTON_GPIO = 16
LED_GPIO = 20
PWM_LED_GPIO = 21
PWM_FREQUENCY = 100         # Hz: high enough not to see the flicker

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

stop = threading.Event()        # set = everybody must finish
active = threading.Event()      # set = the LEDs are working, cleared = both LEDs are off


def button_worker():
    """Input thread: look at the button 50 times per second, switch the LEDs on each press."""
    was_pressed = False
    while not stop.is_set():
        pressed = GPIO.input(BUTTON_GPIO) == GPIO.LOW     # pull-up: LOW means pressed
        if pressed and not was_pressed:                   # react only to the moment of the press
            if active.is_set():
                active.clear()
            else:
                active.set()
            logging.info("LEDs %s", "ON" if active.is_set() else "OFF")
        was_pressed = pressed
        stop.wait(0.02)                                   # sleep 20 ms, but wake up at once on stop


def blink_worker():
    """Output thread 1: blink LED 1 while 'active' is set."""
    while not stop.is_set():
        if active.wait(timeout=0.1):                      # wait up to 100 ms for 'active'
            GPIO.output(LED_GPIO, GPIO.HIGH)
            stop.wait(0.5)
        GPIO.output(LED_GPIO, GPIO.LOW)                   # always off here, also when switched off
        stop.wait(0.5 if active.is_set() else 0)


def fade_worker():
    """Output thread 2: fade LED 2 up and down with PWM while 'active' is set."""
    pwm = GPIO.PWM(PWM_LED_GPIO, PWM_FREQUENCY)           # this thread owns the PWM object
    pwm.start(0)
    try:
        while not stop.is_set():
            if not active.wait(timeout=0.1):
                pwm.ChangeDutyCycle(0)                    # switched off: LED 2 dark
                continue
            for duty in list(range(0, 101, 2)) + list(range(100, -1, -2)):    # 0 -> 100 -> 0 %
                if stop.is_set() or not active.is_set():
                    break
                pwm.ChangeDutyCycle(duty)
                stop.wait(0.02)                           # 50 steps up + 50 down = 2 seconds per cycle
    finally:
        pwm.stop()                                        # must be stopped before GPIO.cleanup()


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_GPIO, GPIO.OUT)
GPIO.setup(PWM_LED_GPIO, GPIO.OUT)

threads = [
    threading.Thread(target=button_worker, name="button"),
    threading.Thread(target=blink_worker, name="blink"),
    threading.Thread(target=fade_worker, name="fade"),
]

try:
    for t in threads:
        t.start()
    logging.info("Press the button to switch the LEDs on / off, Ctrl+C to quit")
    while True:
        time.sleep(1)                                     # the main thread has nothing else to do
except KeyboardInterrupt:
    logging.warning("Stopping")
finally:
    stop.set()
    for t in threads:
        t.join()
    GPIO.cleanup()
    logging.warning("ALL Stopped")

# Things to try:
#  - Run "stress-ng --cpu 4 --timeout 60s" (Linux lab) while the LEDs work: how does the fade change? Why?
#  - Make the fade faster or slower. Which numbers decide the speed?
#  - Make a second button change the blinking speed. Which variable do the threads share?
#  - Why does only the fade thread call the PWM object, and why is the button polled every 20 ms?
