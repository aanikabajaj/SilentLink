# File: db/metadata_logger.py

import psycopg2
import time
from datetime import datetime

# DB connection config
DB_CONFIG = {
    "dbname": "metadata",
    "user": "silentlink_user",
    "password": "ERYx@03_15",  # You can later move this to .env
    "host": "localhost",
    "port": "5432"
}

# SQL to create metadata table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS message_metadata (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    room_id TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
"""

def connect():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("❌ Connection error:", e)
        return None

def ensure_table():
    conn = connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_SQL)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ message_metadata table ensured.")
    except Exception as e:
        print("❌ Table creation error:", e)

def log_message_metadata(user_id, room_id, message, timestamp=None):
    conn = connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        if timestamp is None:
            timestamp = time.time()
        dt = datetime.fromtimestamp(timestamp)
        cur.execute(
            "INSERT INTO message_metadata (user_id, room_id, message, timestamp) VALUES (%s, %s, %s, %s)",
            (user_id, room_id, message, dt)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("📝 Message metadata logged.")
    except Exception as e:
        print("❌ Logging error:", e)

# Run once to create table if needed
if __name__ == "__main__":
    ensure_table()

