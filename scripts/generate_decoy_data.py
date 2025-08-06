# File: scripts/generate_decoy_data.py

import psycopg2
import random
from faker import Faker
from datetime import datetime
import json

fake = Faker()

# Load actual room_ids from session.json
with open("clients/session.json", "r") as f:
    session_data = json.load(f)

# Build a list of (username, room_id) combinations
valid_users = []
for username, data in session_data.get("users", {}).items():
    joined_rooms = data.get("joined_rooms", [])
    for room_id in joined_rooms:
        valid_users.append((username, room_id))

if not valid_users:
    print("❌ No valid users with room_ids found in session.json")
    exit()

# Connect to the decoy PostgreSQL database
conn = psycopg2.connect(
    dbname="decoy", user="silentlink_user", password="ERYx@03_15", host="127.0.0.1"
)
cur = conn.cursor()

# Recreate correct table schema (you can drop if needed)
cur.execute("""
CREATE TABLE IF NOT EXISTS decoy_messages (
    id SERIAL PRIMARY KEY,
    sender TEXT,
    room_id TEXT,
    content TEXT,
    timestamp TIMESTAMP,
    sent BOOLEAN DEFAULT FALSE
)
""")

# Generate and insert fake messages
for _ in range(100):
    sender, room_id = random.choice(valid_users)
    content = fake.sentence()
    timestamp = datetime.utcnow()

    cur.execute("""
    INSERT INTO decoy_messages (sender, room_id, content, timestamp, sent)
    VALUES (%s, %s, %s, %s, FALSE)
    """, (sender, room_id, content, timestamp))

conn.commit()
cur.close()
conn.close()
print("✅ 100 decoy messages inserted.")

