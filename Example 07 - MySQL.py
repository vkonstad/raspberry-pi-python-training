import pymysql
import random
from datetime import datetime

try:
    db_connection = pymysql.connect(host='tpalley.mooo.com', user='labuser', password='labuser123&', database='EmbeddedLab')
    print("Connected to database")

    with db_connection.cursor() as cursor:
        create_table_sql = "CREATE TABLE IF NOT EXISTS Sensor (id INT AUTO_INCREMENT PRIMARY KEY, timestamp DATETIME, temperature FLOAT)"
        cursor.execute(create_table_sql)
        temp_val = random.uniform(30.0, 35.0) 
        current_time = datetime.now()
        insert_sql = "INSERT INTO Sensor (timestamp, temperature) VALUES (%s, %s)"
        cursor.execute(insert_sql, (current_time, temp_val))

    db_connection.commit()
    print(f"Data inserted: Temp={temp_val:.2f} at {current_time}")

except pymysql.MySQLError as e:
    print(f"Database Error: {e}")
    if 'db_connection' in locals() and db_connection.open: 
	    db_connection.rollback()
except Exception as e:
    print(f"General Error: {e}")
finally:
    if 'db_connection' in locals() and db_connection.open:
        db_connection.close()
        print("Connection closed")