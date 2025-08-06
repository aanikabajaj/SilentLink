# File: clients/messaging.py

import requests
import json
import os
import time
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.metadata_logger import log_message_metadata

SESSION_PATH = "clients/session.json"
SERVER_URL = "http://localhost:8008"

def load_session():
    if not os.path.exists(SESSION_PATH):
        return {"users": {}, "active_user": None}
    with open(SESSION_PATH) as f:
        return json.load(f)

def get_active_user():
    session = load_session()
    active = session.get("active_user")
    if not active or active not in session["users"]:
        print("❌ No active user. Please login or switch user.")
        return None
    return session["users"][active]

def send_message():
    user = get_active_user()
    if not user:
        return

    room = input("🔸 Room ID (e.g. !roomid:domain): ").strip()
    message = input("✉️  Message: ").strip()

    url = f"{SERVER_URL}/_matrix/client/v3/rooms/{room}/send/m.room.message?access_token={user['access_token']}"

    payload = {
        "msgtype": "m.text",
        "body": message
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Message sent.")
            log_message_metadata(user["user_id"], room, message, time.time())
        else:
            print(f"❌ Failed to send message: {response.text}")
    except Exception as e:
        print("❌ Error during sending:", e)

def view_messages():
    user = get_active_user()
    if not user:
        return

    room = input("🔸 Room ID to view messages: ").strip()

    url = f"{SERVER_URL}/_matrix/client/v3/rooms/{room}/messages?access_token={user['access_token']}&dir=b&limit=5"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("\n🗨️  Last 5 messages:")
            for event in reversed(data.get("chunk", [])):
                sender = event.get("sender")
                body = event.get("content", {}).get("body")
                print(f"👤 {sender}: {body}")
        else:
            print(f"❌ Failed to fetch messages: {response.text}")
    except Exception as e:
        print("❌ Error during fetching:", e)

