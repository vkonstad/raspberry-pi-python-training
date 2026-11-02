# Example 12 - CPU Temperature to SQLite
# Stores the CPU temperature of the Raspberry Pi in a local SQLite database file.
# SQLite needs no server: the whole database is one file (temperature.db, next to this script).
#
# Run once, store one reading:          python3 "Example 12 - CPU Temperature to SQLite.py"
# Keep running, one reading every 10 s: python3 "Example 12 - CPU Temperature to SQLite.py" --every 10
# Look at the stored data:              sqlite3 temperature.db "SELECT * FROM cpu_temperature;"
#   (sudo apt install sqlite3 for the sqlite3 command)
#
# Messages are written with the logging module to the standard output, with a time and a level:
#   - from a terminal you see them on screen
#   - from cron, redirect them:  ... >> /home/pi/cron.log 2>&1
#   - from systemd they end up in the journal:  journalctl -u <service name> -f
# Set LOG_LEVEL=DEBUG in the environment to see more detail.
#
# Used by the cron and systemd tasks of "Linux lab.md".
#
# Concepts: sqlite3 module, logging, reading a system file, command-line arguments, loop with sleep

import logging
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("cpu_temperature")

# The database lives next to the script, with an absolute path.
# (cron and systemd do not start in your folder, so never rely on relative paths)
DB_FILE = Path(__file__).resolve().parent / "temperature.db"

# Linux exposes the CPU temperature as a file, in thousandths of a degree Celsius
THERMAL_FILE = Path("/sys/class/thermal/thermal_zone0/temp")

WARNING_TEMPERATURE = 70.0      # degrees Celsius, above this we log a warning


def read_cpu_temperature():
    return int(THERMAL_FILE.read_text()) / 1000


def store(temperature, db_file=DB_FILE):
    # "with connection" commits the transaction on success and rolls back on error
    connection = sqlite3.connect(db_file)
    try:
        with connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS cpu_temperature "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, celsius REAL)"
            )
            connection.execute(
                "INSERT INTO cpu_temperature (timestamp, celsius) VALUES (?, ?)",
                (datetime.now().isoformat(timespec="seconds"), temperature),
            )
    finally:
        connection.close()


def record_once():
    temperature = read_cpu_temperature()
    log.debug("Read %.1f C from %s", temperature, THERMAL_FILE)
    store(temperature)
    if temperature >= WARNING_TEMPERATURE:
        log.warning("CPU is hot: %.1f C", temperature)
    log.info("Stored %.1f C in %s", temperature, DB_FILE)


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--every":
        period = float(sys.argv[2])
        log.info("Started, one reading every %s s (Ctrl+C to stop)", period)
        while True:
            try:
                record_once()
            except sqlite3.Error:
                # a temporary problem (e.g. the database is locked): log it and try again next time
                log.exception("Could not write to the database")
            time.sleep(period)
    else:
        record_once()


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        log.error("Cannot read %s: this example must run on the Raspberry Pi (Linux).", THERMAL_FILE)
        sys.exit(1)
    except KeyboardInterrupt:
        log.info("Stopped")
    except Exception:
        log.exception("Unexpected error")
        sys.exit(1)
