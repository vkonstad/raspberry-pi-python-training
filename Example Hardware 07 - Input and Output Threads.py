# Example Hardware 07 - Input and Output Threads
# A button (input) and an LED (output) handled by two different threads, while the
# main thread only keeps the program alive. Each button press switches the blinking on or off.
# Same wiring as Example Hardware 04-06: button on BUTTON_GPIO (pull-up), LED on LED_GPIO.
# Stop with Ctrl+C.
#
# Concepts: threading (Example 08), threading.Event for communication and stopping,
#           logging with the thread name, polling an input, GPIO cleanup in finally

import logging
import threading
import time
import RPi.GPIO as GPIO

BUTTON_GPIO = 16
LED_GPIO = 20

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')

stop = threading.Event()        # set = everybody must finish
blinking = threading.Event()    # set = the LED should blink, cleared = the LED stays off


def button_worker():
    """Input thread: look at the button 50 times per second, toggle blinking on each press."""
    was_pressed = False
    while not stop.is_set():
        pressed = GPIO.input(BUTTON_GPIO) == GPIO.LOW     # pull-up: LOW means pressed
        if pressed and not was_pressed:                   # react only to the moment of the press
            if blinking.is_set():
                blinking.clear()
            else:
                blinking.set()
            logging.info("Blinking %s", "ON" if blinking.is_set() else "OFF")
        was_pressed = pressed
        stop.wait(0.02)                                   # sleep 20 ms, but wake up at once on stop


def led_worker():
    """Output thread: blink the LED while 'blinking' is set."""
    while not stop.is_set():
        if blinking.wait(timeout=0.1):                    # wait up to 100 ms for 'blinking'
            GPIO.output(LED_GPIO, GPIO.HIGH)
            stop.wait(0.5)
        GPIO.output(LED_GPIO, GPIO.LOW)                   # always off here, also when blinking was switched off
        stop.wait(0.5 if blinking.is_set() else 0)


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_GPIO, GPIO.OUT)

threads = [
    threading.Thread(target=button_worker, name="button"),
    threading.Thread(target=led_worker, name="led"),
]

try:
    for t in threads:
        t.start()
    logging.info("Press the button to start / stop the blinking, Ctrl+C to quit")
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
#  - Make a second button change the blinking speed. Which variable do the two threads share?
#  - Count the presses and log the total when the program stops.
#  - Why is the button polled every 20 ms? What happens with time.sleep(1) instead?
