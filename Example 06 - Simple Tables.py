# Example 06 - Simple Tables
# Reads the tab-separated file sample.csv, first by hand, then with pandas,
# and plots the temperatures.
# Note: plt.show() needs a screen, so run this on a PC or a Pi with a desktop.
#
# Concepts: files, with, string split, pandas DataFrame, plotting

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

script_dir = Path(__file__).resolve().parent
print(script_dir)

# 1. By hand: read the file and split every line on the TAB character
with open(script_dir / "sample.csv", "r") as f:
    contents = f.read()
print(contents)

for line in contents.splitlines():
    print(line.split('\t'))

# 2. With pandas: one line does the same job (the file uses tabs, not commas)
df = pd.read_csv(script_dir / "sample.csv", sep='\t')
print(df)

df.plot(x='time', y=['tavg', 'tmin', 'tmax'])
plt.show()
