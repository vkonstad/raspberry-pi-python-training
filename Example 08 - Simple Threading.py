# Example 08 - Simple Threading
# Two worker threads and the main thread run at the same time, each at its own pace.
# Press Ctrl+C to stop everything cleanly.
#
# Concepts: threading.Thread, threading.Event as a stop flag, logging, join()

import logging
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

stop_event = threading.Event()


def worker(name, period):
    # wait() sleeps like time.sleep(), but wakes up immediately when the event is set
    while not stop_event.wait(period):
        logging.info(name)


threads = [
    threading.Thread(target=worker, args=("worker1", 1)),
    threading.Thread(target=worker, args=("worker2", 1.75)),
]
for t in threads:
    t.start()

try:
    while True:
        logging.info("MAIN thread")
        stop_event.wait(5)
except KeyboardInterrupt:
    logging.warning('Stopping')
    stop_event.set()

for t in threads:
    t.join()
logging.warning('ALL Stopped')
