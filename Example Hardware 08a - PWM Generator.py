# Example Hardware 08a - PWM Generator
# Generates a PWM signal on one pin, with the same frequency either by SOFTWARE PWM
# (RPi.GPIO, timed by the CPU) or by the HARDWARE PWM of the chip (pigpio, timed by the hardware).
# An input chooses which one: a wire (or a switch) from SELECT_GPIO to GND = hardware, open = software.
# Measure the signal on the neighbour's Pi with Example Hardware 08b and compare the two modes.
# Stop with Ctrl+C.
#
# Needs the pigpio daemon:
#   sudo apt install pigpio python3-pigpio
#   sudo systemctl enable --now pigpiod
#
# Concepts: software and hardware PWM, using two libraries for the same pin (one at a time),
#           reading an input to change the behaviour, cleanup in finally

import sys
import time
import pigpio
import RPi.GPIO as GPIO

PWM_GPIO = 12               # one of the pins with hardware PWM: 12, 13, 18, 19
FREQUENCY = 100             # Hz, the same in both modes
DUTY_CYCLE = 50             # % of the period the output is high
SELECT_GPIO = 23            # to GND = hardware PWM, open = software PWM

pi = pigpio.pi()
if not pi.connected:
    sys.exit("Cannot connect to the pigpio daemon. Start it with:  sudo systemctl enable --now pigpiod")

GPIO.setmode(GPIO.BCM)
GPIO.setup(SELECT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class PwmOutput:
    """One pin, one frequency, two ways of producing it. Only one of them uses the pin at a time."""

    def __init__(self):
        self.mode = None
        self._software = None

    def use(self, mode):
        if mode == self.mode:
            return
        self._stop()
        if mode == "hardware":
            pi.hardware_PWM(PWM_GPIO, FREQUENCY, DUTY_CYCLE * 10000)    # pigpio duty: 0 to 1000000
        else:
            GPIO.setup(PWM_GPIO, GPIO.OUT)
            self._software = GPIO.PWM(PWM_GPIO, FREQUENCY)
            self._software.start(DUTY_CYCLE)
        self.mode = mode
        print(f"{mode.upper()} PWM: {FREQUENCY} Hz, duty {DUTY_CYCLE}% on GPIO{PWM_GPIO}")

    def _stop(self):
        if self.mode == "software":
            self._software.stop()
            GPIO.cleanup(PWM_GPIO)                  # give the pin back before pigpio uses it
        elif self.mode == "hardware":
            pi.hardware_PWM(PWM_GPIO, 0, 0)         # 0 Hz = stop the hardware PWM
        self.mode = None

    def close(self):
        self._stop()


output = PwmOutput()

try:
    print(f"GPIO{SELECT_GPIO} to GND = hardware PWM, open = software PWM (Ctrl+C to stop)")
    while True:
        wanted = "hardware" if GPIO.input(SELECT_GPIO) == GPIO.LOW else "software"
        output.use(wanted)                          # does nothing if the mode did not change
        time.sleep(0.2)                             # reading the selector 5 times a second is enough
except KeyboardInterrupt:
    print()
finally:
    output.close()
    GPIO.cleanup()
    pi.stop()

# Things to try:
#  - Run Example Hardware 08b on the neighbour's Pi and switch between the two modes. What changes?
#  - Run "stress-ng --cpu 4 --timeout 60s" on this Pi in each mode. What happens to the signal?
#  - Why can RPi.GPIO and pigpio not both drive the same pin at the same time?
#  - Why are only the pins 12, 13, 18 and 19 used for the hardware PWM?
