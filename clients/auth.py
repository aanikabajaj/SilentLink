# File: clients/auth.py

import requests
import json
import os

SESSION_PATH = "clients/session.json"
SERVER_URL = "http://localhost:8008"

def load_session():
    if os.path.exists(SESSION_PATH):
        with open(SESSION_PATH) as f:
            return json.load(f)
    return {"users": {}, "active_user": None}

def save_session(data):
    with open(SESSION_PATH, "w") as f:
        json.dump(data, f, indent=2)

def login_user(username=None, password=None):
    if username is None:
        username = input("Username: ").strip()
    if password is None:
        password = input("Password: ").strip()

    payload = {
        "type": "m.login.password",
        "user": username,
        "password": password
    }

    try:
        resp = requests.post(f"{SERVER_URL}/_matrix/client/v3/login", json=payload)
        if resp.status_code == 200:
            data = resp.json()
            access_token = data.get("access_token")
            print(f"✅ Access token retrieved for {username}")

            # Save/update session.json
            session = load_session()
            session["users"][username] = {
                "access_token": access_token,
                "user_id": data["user_id"],
                "device_id": data["device_id"]
            }
            session["active_user"] = username
            save_session(session)

        else:
            print(f"❌ Failed to login: {username}: {resp.text}")
    except Exception as e:
        print("❌ Exception during login:", e)

def switch_active_user():
    session = load_session()
    users = session.get("users", {})
    if not users:
        print("❌ No users found in session.json. Please login first.")
        return

    print("📋 Available users:")
    for idx, user in enumerate(users.keys(), 1):
        print(f"{idx}. {user}")

    try:
        choice = int(input("Select user number: "))
        selected_user = list(users.keys())[choice - 1]
        session["active_user"] = selected_user
        save_session(session)
        print(f"✅ Active user set to: {selected_user}")
    except Exception:
        print("❌ Invalid selection.")

