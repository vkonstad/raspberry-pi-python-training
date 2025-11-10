from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

script_dir = Path(__file__).resolve().parent
print(script_dir)
f = open(script_dir / "sample.csv", "r")
contents = f.read()
f.close()
print(contents)
lines = contents.split('\n')
for line in lines:
    print(line.split('\t'))

df = pd.read_csv(script_dir / "sample.csv", sep='\t')
print(df)

df.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()