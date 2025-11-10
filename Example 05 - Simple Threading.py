import logging
import threading
import time

def worker1(arg):
    while not arg["stop"]:
        logging.info("worker1")
        time.sleep(1)

def worker2(arg):
    while not arg["stop"]:
        logging.info("worker2")
        time.sleep(1.75)


logging.basicConfig(level=logging.INFO, format="%(message)s")
parameters = {"stop": False}
thread = threading.Thread(target=worker1, args=(parameters,))
thread_two = threading.Thread(target=worker2, args=(parameters,))
thread.start()
thread_two.start()

while True:
    try:
        logging.info("MAIN thread")
        time.sleep(5)
    except KeyboardInterrupt:
        parameters["stop"] = True
        logging.info('Stopping')
        break
thread.join()
thread_two.join()