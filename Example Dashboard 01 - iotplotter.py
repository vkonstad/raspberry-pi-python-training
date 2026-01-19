import time, random
from urllib import request

lines = []
lines.append("{0},Temperature,{1}".format(time.time(), random.randrange(20,22)))
lines.append("{0},Humidity,{1}".format(time.time(), random.randrange(60,80)))
lines.append("{0},Battery,{1}".format(time.time(), random.randrange(90,100)))
lines = "\n".join(lines)
req = request.Request("https://iotplotter.com/api/v2/feed/191247582110697872.csv",data=lines.encode(),headers={"api-key": 'e9e559827d85b3122820e361d1bf82cbd66a64c4e8'})
print(lines)
request.urlopen(req).read()
print("sent.")