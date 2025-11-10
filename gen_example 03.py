import matplotlib.pyplot as plt
import pandas as pd


f = open("D:\Πανεπιστήμιο\Διδασκαλία\Μεταπτυχιακό\Ενσωματωμένα Συστήματα\python\sample.csv", "r")
contents = f.read()
f.close()
print(contents)
lines = contents.split('\n')
for line in lines:
    print(line.split('\t'))



# df = pd.read_csv("D:\Πανεπιστήμιο\Διδασκαλία\Μεταπτυχιακό\Ενσωματωμένα Συστήματα\python\sample.csv", sep='\t')
# print(df)

# df.plot(y=['tavg', 'tmin', 'tmax'])
# plt.show()