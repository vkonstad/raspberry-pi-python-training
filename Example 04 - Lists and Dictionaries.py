# Example 04 - Lists and Dictionaries
# The two data structures you will use all the time: a list keeps things in order,
# a dictionary finds things by name. Here: a few temperature readings from sensors.
#
# Concepts: list, dict, loops over both, list comprehension, sorting, min/max/sum

# A list: ordered, accessed by position (starting from 0)
temperatures = [21.5, 22.0, 19.8, 23.1, 22.7]

print("First reading:", temperatures[0])
print("Last reading :", temperatures[-1])
print("Number of readings:", len(temperatures))

temperatures.append(24.0)           # add a new reading at the end
print("Min / Max / Average:", min(temperatures), max(temperatures),
      round(sum(temperatures) / len(temperatures), 2))
print("Sorted:", sorted(temperatures))

# A list comprehension builds a new list from an old one
fahrenheit = [round(t * 9 / 5 + 32, 1) for t in temperatures]
print("In Fahrenheit:", fahrenheit)
warm = [t for t in temperatures if t > 22]
print("Warmer than 22:", warm)

print()

# A dictionary: pairs of key -> value, accessed by key
reading = {"sensor": "living_room", "temperature": 22.5, "humidity": 48}

print("Sensor:", reading["sensor"])
reading["battery"] = 97                     # add a new key
reading["temperature"] = 22.8               # change an existing one
print("Humidity or 0 if missing:", reading.get("humidity", 0))

for key, value in reading.items():
    print(f"  {key:<12} = {value}")

print()

# The two combined: a list of dictionaries is how most real data looks (rows of a table)
readings = [
    {"sensor": "living_room", "temperature": 22.5},
    {"sensor": "kitchen", "temperature": 25.1},
    {"sensor": "garage", "temperature": 17.3},
    {"sensor": "kitchen", "temperature": 24.7},
]

# Group the temperatures by sensor
by_sensor = {}
for r in readings:
    by_sensor.setdefault(r["sensor"], []).append(r["temperature"])

for sensor, values in by_sensor.items():
    print(f"{sensor:<12} {len(values)} reading(s), average {sum(values) / len(values):.1f}")

hottest = max(readings, key=lambda r: r["temperature"])
print("Hottest reading:", hottest)
