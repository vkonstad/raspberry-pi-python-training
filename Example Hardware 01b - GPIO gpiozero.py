# Example Hardware 01b - GPIO with gpiozero
# The same LED blink as "Example Hardware 01 - GPIO.py", written with the gpiozero library.
# Compare the two: gpiozero hides the setup (mode, direction) and the cleanup.
# gpiozero comes with Raspberry Pi OS (otherwise: sudo apt install python3-gpiozero).
# Stop the program with Ctrl+C.

from time import sleep
from gpiozero import LED

# Pin definition
led_pin = 12

# One line replaces GPIO.setmode() and GPIO.setup(): "this pin is an LED"
led = LED(led_pin)

# Blink forever
try:
    while True:
        led.on()        # Turn LED on
        sleep(1)        # Delay for 1 second
        led.off()       # Turn LED off
        sleep(1)        # Delay for 1 second
except KeyboardInterrupt:
    pass                # no GPIO.cleanup() needed: gpiozero releases the pin when the program ends

# The same blinking, without writing the loop: gpiozero does it in a background thread
#
#   from signal import pause
#   led.blink(on_time=1, off_time=1)
#   pause()
