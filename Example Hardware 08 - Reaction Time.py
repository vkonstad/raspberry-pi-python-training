# Example Hardware 08 - Reaction Time
# A small game: wait for the LED to light up (after a random time) and press the button
# as fast as you can. Five rounds are measured, saved in a CSV file and summarised.
# Same wiring as Example Hardware 04-06: button on BUTTON_GPIO (pull-up), LED on LED_GPIO.
# Pressing before the LED lights up does not count: the round is repeated.
#
# Concepts: input and output together, random, timing, waiting for a button edge with a timeout,
#           lists and statistics (Example 04), saving to CSV (Example 05), cleanup in finally

import csv
import random
import statistics
import time
from datetime import datetime
from pathlib import Path
import RPi.GPIO as GPIO

BUTTON_GPIO = 16
LED_GPIO = 20

ROUNDS = 5
TIMEOUT_MS = 3000       # a round is lost if the button is not pressed within 3 seconds
CSV_FILE = Path(__file__).resolve().parent / "output" / "reaction_times.csv"


def play_round():
    """Returns the reaction time in ms, or None if the player was too early or too slow."""
    GPIO.output(LED_GPIO, GPIO.LOW)
    wait_ms = random.randint(2000, 5000)

    # The button must NOT be pressed while we wait: wait_for_edge returns None when the time is up
    if GPIO.wait_for_edge(BUTTON_GPIO, GPIO.FALLING, timeout=wait_ms) is not None:
        print("Too early! Wait for the LED.")
        return None

    GPIO.output(LED_GPIO, GPIO.HIGH)
    start = time.perf_counter()
    pressed = GPIO.wait_for_edge(BUTTON_GPIO, GPIO.FALLING, timeout=TIMEOUT_MS)
    reaction_ms = (time.perf_counter() - start) * 1000
    GPIO.output(LED_GPIO, GPIO.LOW)

    if pressed is None:
        print("Too slow!")
        return None
    return reaction_ms


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_GPIO, GPIO.OUT)

results = []        # the reaction times, in ms

try:
    print(f"{ROUNDS} rounds. Press the button as soon as the LED lights up. Ctrl+C to quit.")
    while len(results) < ROUNDS:
        reaction = play_round()
        if reaction is not None:
            results.append(reaction)
            print(f"Round {len(results)}: {reaction:.0f} ms")
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted")
finally:
    GPIO.cleanup()

if results:
    print()
    print(f"Best {min(results):.0f} ms, average {statistics.mean(results):.0f} ms, "
          f"median {statistics.median(results):.0f} ms")

    CSV_FILE.parent.mkdir(exist_ok=True)
    new_file = not CSV_FILE.exists()
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["time", "round", "reaction_ms"])
        now = datetime.now().isoformat(timespec="seconds")
        for number, reaction in enumerate(results, start=1):
            writer.writerow([now, number, round(reaction)])
    print("Saved in", CSV_FILE)

# Things to try:
#  - Show the best result of ALL the games, reading the CSV file back.
#  - Why does GPIO.wait_for_edge need a timeout? What would happen without it?
#  - Add a second player with a second button.
