import time, random
from urllib import request

lines = []
lines.append("{0},Temperature,{1}".format(time.time(), random.randrange(20,22)))
lines.append("{0},Humidity,{1}".format(time.time(), random.randrange(60,80)))
lines.append("{0},Battery,{1}".format(time.time(), random.randrange(90,100)))
lines = "\n".join(lines)
req = request.Request("https://iotplotter.com/api/v2/feed/your_id.csv",data=lines.encode(),headers={"api-key": 'your_api_key'})
print(lines)
request.urlopen(req).read()
print("sent.")