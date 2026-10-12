# Example 10 - MySQL
# Inserts one random "sensor" reading into a table of a local MySQL database.
# Install MySQL and run mysql_setup.sql first (see README). Connection settings: db_config.py
#
# Concepts: database connection, SQL, parameterized queries, commit/rollback, error handling

import pymysql
import random
from datetime import datetime

from db_config import DB_CONFIG

db_connection = None

try:
    db_connection = pymysql.connect(**DB_CONFIG)
    print("Connected to database")

    with db_connection.cursor() as cursor:
        create_table_sql = "CREATE TABLE IF NOT EXISTS Sensor (id INT AUTO_INCREMENT PRIMARY KEY, timestamp DATETIME, temperature FLOAT)"
        cursor.execute(create_table_sql)

        temp_val = random.uniform(30.0, 35.0)
        current_time = datetime.now()
        # %s placeholders: the driver inserts the values safely (never build SQL with f-strings)
        insert_sql = "INSERT INTO Sensor (timestamp, temperature) VALUES (%s, %s)"
        cursor.execute(insert_sql, (current_time, temp_val))

    db_connection.commit()
    print(f"Data inserted: Temp={temp_val:.2f} at {current_time}")

except pymysql.MySQLError as e:
    print(f"Database Error: {e}")
    if db_connection is not None and db_connection.open:
        db_connection.rollback()
finally:
    if db_connection is not None and db_connection.open:
        db_connection.close()
        print("Connection closed")
