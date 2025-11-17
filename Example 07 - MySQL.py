import pymysql, random
from datetime import datetime
import pandas

try:
    db_connection = pymysql.connect(host='tpalley.mooo.com', user='labuser', password='labuser123&', database='EmbeddedLab')
    print("Connected")
except Exception as e:
    print("Can't connect to database")
    print(e)
    exit()

mycursor = db_connection.cursor()
mycursor.execute("SHOW TABLES LIKE 'Sensor'")
result = mycursor.fetchone()
if result: pass
else: mycursor.execute("CREATE TABLE Sensor (timestamp datetime, temperature float)")

tDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
mycursor.execute("INSERT INTO Sensor (timestamp, temperature) VALUES (%s, %s)", (tDate, str(random.randint(30,35))))
db_connection.commit()

# mycursor.execute("SELECT * from Sensor")
# result = mycursor.fetchall()
# print('Last measurement is:', result[-1])
# print('Number of measurements: ', len(result))
# print('')

# mycursor.execute("SELECT * from Sensor order by timestamp ASC limit 1")
# result = mycursor.fetchall()
# print('FIRST result', result)
# print('')

# mycursor.execute("SELECT * from Sensor order by timestamp DESC limit 1")
# result = mycursor.fetchall()
# print('LAST result', result)
# print('')

# mycursor.execute("SELECT * from Sensor order by temperature DESC limit 1")
# result = mycursor.fetchall()
# print('BIGGEST temperature', result)
# print('')

# mycursor.execute("SELECT * from Sensor where temperature > 25")
# result = mycursor.fetchall()
# df = pandas.DataFrame(result)
# print (df)
# print('')

# mycursor.execute("SELECT AVG(temperature) from Sensor")
# result = mycursor.fetchall()
# print('AVERAGE result', result)
# print('')

# mycursor.execute("SELECT * from Sensor")
# result = mycursor.fetchall()
# df = pandas.DataFrame(result)
# print ('DF mean value ', df[1].mean())
# print('')

result_dataFrame = pandas.read_sql("SELECT * from Sensor", db_connection)
print(result_dataFrame)

# Closing Database Connection 
db_connection.close()