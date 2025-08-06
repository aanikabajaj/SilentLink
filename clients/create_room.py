# File: clients/create_room.py

import requests
import json
import os

SERVER_URL = "http://localhost:8008"
SESSION_PATH = "clients/session.json"

# Check session
if not os.path.exists(SESSION_PATH):
    print("❌ session.json not found. Please login/register first.")
    exit(1)

with open(SESSION_PATH) as f:
    session = json.load(f)

active_username = session.get("active_user")
users = session.get("users", {})

if not active_username or active_username not in users:
    print("❌ Active user not set or missing in session.")
    exit(1)

access_token = users[active_username].get("access_token")
if not access_token:
    print(f"❌ Access token missing for user '{active_username}'. Please login again.")
    exit(1)

# Prompt for room name and invitees
room_name = input("🏷️ Enter room name (optional): ").strip()
invite_list = input("👥 Enter comma-separated usernames to invite (e.g. @bob:localhost): ").strip()

invitees = [user.strip() for user in invite_list.split(",") if user.strip()]
invitees_mxids = []

# Convert to MXIDs if not already
for user in invitees:
    if not user.startswith("@"):
        user = f"@{user}:localhost"
    invitees_mxids.append(user)

# Construct request payload
payload = {
    "invite": invitees_mxids,
}
if room_name:
    payload["name"] = room_name
    payload["preset"] = "private_chat"

url = f"{SERVER_URL}/_matrix/client/v3/createRoom?access_token={access_token}"
res = requests.post(url, json=payload)

if res.status_code == 200:
    room_id = res.json().get("room_id")
    print(f"✅ Room created successfully!\nRoom ID: {room_id}")

    # Store room in session
    users[active_username].setdefault("rooms", []).append({
        "room_id": room_id,
        "name": room_name or "(Unnamed Room)",
        "invitees": invitees_mxids
    })
    with open(SESSION_PATH, "w") as f:
        json.dump(session, f, indent=2)

else:
    print("❌ Failed to create room:", res.status_code)
    print(res.text)

