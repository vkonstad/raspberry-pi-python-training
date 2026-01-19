import streamlit as st
import pymysql
import pandas as pd
import random
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'localuser',
    'password': 'localuser124!',
    'database': 'exampledb'
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS measurements (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    temperature FLOAT
                ) ENGINE=InnoDB;
            """)
        conn.commit()
    finally:
        conn.close()

def insert_reading(temp_value):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            timestamp = datetime.now()
            sql = "INSERT INTO measurements (timestamp, temperature) VALUES (%s, %s)"
            cursor.execute(sql, (timestamp, temp_value))
        conn.commit()
    finally:
        conn.close()

def fetch_data():
    conn = get_connection()
    try:
        return pd.read_sql("SELECT timestamp, temperature FROM measurements ORDER BY timestamp ASC", conn)
    except:
        return pd.DataFrame()
    finally:
        conn.close()

init_db()

st.title("Sensor Monitor")

if st.button("Add Measurement"):
    new_temp = round(random.uniform(20.0, 30.0), 2)
    insert_reading(new_temp)
    st.success(f"Added: {new_temp} C")

df = fetch_data()

if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    st.subheader("Temperature Graph")
    st.line_chart(df.set_index('timestamp'))
    
    st.subheader("Recent Data")
    st.dataframe(df.sort_values(by='timestamp', ascending=False).head(5), use_container_width=True)
else:
    st.write("No data available.")