# Example Hardware 08b - PWM Frequency Measurement
# Measures a signal that arrives on one input pin and prints, every 10 seconds:
#   - the frequency from the NUMBER of edges in the window
#   - the frequency and the JITTER from the TIME between consecutive edges (the periods)
#   - the CPU load
# Connect the output pin of the neighbour's Pi (running Example Hardware 08a) to INPUT_GPIO,
# and connect the GND pins of the two Pis together. Stop with Ctrl+C.
#
# The time of every edge is taken with a Python clock. Choose which one on the command line:
#   python3 "Example Hardware 08b - PWM Frequency Measurement.py" perf_counter_ns
#   (time_ns, monotonic_ns or perf_counter_ns; perf_counter_ns is the default)
#
# Concepts: counting edges vs timing periods, mean and standard deviation (jitter),
#           clocks in Python (time.get_clock_info), command-line arguments, threading.Lock

import os
import statistics
import sys
import threading
import time
from datetime import datetime
import RPi.GPIO as GPIO

INPUT_GPIO = 16
WINDOW_S = 10               # one result every this many seconds

# The clocks to compare: name -> (function returning nanoseconds, name for time.get_clock_info)
CLOCKS = {
    "time_ns": (time.time_ns, "time"),
    "monotonic_ns": (time.monotonic_ns, "monotonic"),
    "perf_counter_ns": (time.perf_counter_ns, "perf_counter"),
}

clock_name = sys.argv[1] if len(sys.argv) > 1 else "perf_counter_ns"
if clock_name not in CLOCKS:
    sys.exit(f"Unknown clock '{clock_name}'. Choose one of: {', '.join(CLOCKS)}")
clock, info_name = CLOCKS[clock_name]
info = time.get_clock_info(info_name)


class EdgeRecorder:
    """Keeps the time of every rising edge. The callback runs in another thread: a lock protects the list."""

    def __init__(self):
        self._lock = threading.Lock()
        self._timestamps = []

    def record(self, channel):
        now = clock()                       # the very first thing: take the time
        with self._lock:
            self._timestamps.append(now)

    def take(self):
        """Returns the times recorded so far and starts with an empty list."""
        with self._lock:
            timestamps, self._timestamps = self._timestamps, []
            return timestamps


recorder = EdgeRecorder()

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# No bouncetime here: we want every single edge
GPIO.add_event_detect(INPUT_GPIO, GPIO.RISING, callback=recorder.record)

print(f"Measuring GPIO{INPUT_GPIO} with {clock_name}, one result every {WINDOW_S} seconds (Ctrl+C to stop)")
print(f"Clock {info_name}: implementation={info.implementation}, resolution={info.resolution}, "
      f"monotonic={info.monotonic}, adjustable={info.adjustable}")

try:
    while True:
        recorder.take()                                 # forget what was recorded before
        start = clock()
        time.sleep(WINDOW_S)
        stamps = recorder.take()
        elapsed_s = (clock() - start) / 1e9             # the real duration of the window
        edges = len(stamps)

        line = f"{datetime.now():%H:%M:%S}  edges={edges:5d}  count={edges / elapsed_s:7.2f} Hz"
        if edges >= 3:
            periods_ms = [(b - a) / 1e6 for a, b in zip(stamps, stamps[1:])]
            mean_ms = statistics.mean(periods_ms)
            line += (f"  | period={mean_ms:7.3f} ms ({1000 / mean_ms:7.2f} Hz)"
                     f"  jitter(std)={statistics.stdev(periods_ms):6.3f} ms"
                     f"  min={min(periods_ms):7.3f}  max={max(periods_ms):7.3f} ms")
        line += f"  | load={os.getloadavg()[0]:.2f}"
        print(line)
except KeyboardInterrupt:
    print()
finally:
    GPIO.cleanup()

# Things to try:
#  - Software PWM or hardware PWM at the neighbour: which number changes, the count or the jitter? Why?
#  - Run "stress-ng --cpu 4 --timeout 60s" on the Pi that GENERATES, then on the Pi that MEASURES.
#    Which one disturbs the result, and which numbers show it?
#  - Run the script with each clock. Do the results change? What do the clock infos say?
#  - A lost edge makes one period twice as long. Where do you see it: count, period mean, or max?
