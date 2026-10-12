# Example 05 - JSON and CSV
# Saves a list of readings (see Example 04) to a JSON file and to a CSV file,
# then reads them back. JSON keeps the structure (nested data), CSV is a flat table
# that opens in Excel. Output files are written next to this script, in "output/".
#
# Concepts: json module, csv module, files with "with", pathlib, round trip (write -> read)

import csv
import json
from datetime import datetime
from pathlib import Path
import random

output_dir = Path(__file__).resolve().parent / "output"
output_dir.mkdir(exist_ok=True)

# Some made-up sensor data: a list of dictionaries
readings = [
    {
        "time": datetime.now().isoformat(timespec="seconds"),
        "sensor": random.choice(["living_room", "kitchen", "garage"]),
        "temperature": round(random.uniform(17, 26), 1),
    }
    for _ in range(5)
]

# --- JSON ---
json_file = output_dir / "readings.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(readings, f, indent=2)        # indent makes the file human readable

with open(json_file, "r", encoding="utf-8") as f:
    from_json = json.load(f)
print("Read from JSON:", len(from_json), "readings, first one:", from_json[0])

# --- CSV ---
csv_file = output_dir / "readings.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["time", "sensor", "temperature"])
    writer.writeheader()
    writer.writerows(readings)

with open(csv_file, "r", newline="", encoding="utf-8") as f:
    from_csv = list(csv.DictReader(f))
print("Read from CSV :", len(from_csv), "readings, first one:", from_csv[0])

# Difference to notice: CSV has no types, everything comes back as text
print("Type of temperature in JSON:", type(from_json[0]["temperature"]).__name__)
print("Type of temperature in CSV :", type(from_csv[0]["temperature"]).__name__)

average = sum(float(r["temperature"]) for r in from_csv) / len(from_csv)
print(f"Average temperature: {average:.1f}")
print("Files written in:", output_dir)
