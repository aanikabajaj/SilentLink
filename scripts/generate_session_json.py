# File: scripts/generate_session_json.py

import requests
import json

server_url = "http://localhost:8008"

users = [
    {"username": "alice", "password": "alice_pass"},
    {"username": "bob", "password": "bob_pass"},
    {"username": "charlie", "password": "charlie_pass"},
    {"username": "david", "password": "david_pass"},
    {"username": "eve", "password": "eve_pass"}
]

session = {"users": {}, "active_user": "alice"}

for user in users:
    payload = {
        "type": "m.login.password",
        "user": user["username"],
        "password": user["password"]
    }

    resp = requests.post(f"{server_url}/_matrix/client/r0/login", json=payload)

    if resp.status_code == 200:
        data = resp.json()
        session["users"][user["username"]] = {
            "user_id": data["user_id"],
            "access_token": data["access_token"]
        }
        print(f"✅ Access token retrieved for {user['username']}")
    else:
        print(f"❌ Failed to login: {user['username']}: {resp.text}")

# Save to session.json
with open("clients/session.json", "w") as f:
    json.dump(session, f, indent=2)
    print("\n📁 session.json saved in clients/")

