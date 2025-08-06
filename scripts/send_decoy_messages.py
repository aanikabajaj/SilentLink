# File: scripts/send_decoy_messages.py

import psycopg2
import json
import requests
import random
from time import sleep

# Load user sessions
with open("clients/session.json", "r") as f:
    session_data = json.load(f)
    sessions = [
        {"username": username, "access_token": data["access_token"]}
        for username, data in session_data["users"].items()
    ]
    valid_usernames = [u["username"] for u in sessions]  # ✅ Valid senders

# Database connection
conn = psycopg2.connect(
    dbname="decoy",
    user="silentlink_user",
    password="ERYx@03_15",
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()

# Fetch unsent decoy messages only from valid senders
cur.execute("""
    SELECT id, sender, room_id, content 
    FROM decoy_messages 
    WHERE sent IS FALSE 
    AND sender = ANY(%s) 
    LIMIT 5
""", (valid_usernames,))
messages = cur.fetchall()

server_url = "http://localhost:8008"

for msg in messages:
    msg_id, sender, room_id, content = msg

    # Get access token for sender
    user_session = next((u for u in sessions if u["username"] == sender), None)
    if not user_session:
        print(f"❌ No session found for user: {sender}")
        continue

    token = user_session["access_token"]
    txn_id = str(random.randint(100000, 999999))

    # Send message to room
    url = f"{server_url}/_matrix/client/v3/rooms/{room_id}/send/m.room.message/{txn_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "msgtype": "m.text",
        "body": content
    }

    res = requests.put(url, headers=headers, json=payload)
    if res.status_code == 200:
        print(f"✅ Sent decoy message from {sender} to {room_id}")
        # Mark message as sent
        cur.execute("UPDATE decoy_messages SET sent = TRUE WHERE id = %s", (msg_id,))
        conn.commit()
    else:
        print(f"❌ Failed to send message: {res.text}")

    sleep(1)  # avoid flooding

cur.close()
conn.close()

