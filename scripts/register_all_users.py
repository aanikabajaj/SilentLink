import requests
import json
import hmac
import hashlib
import base64
import time

shared_secret = "ERYx@03_15"
server_url = "http://localhost:8008"

users = [
    {"username": "alice", "password": "alice_pass"},
    {"username": "bob", "password": "bob_pass"},
    {"username": "charlie", "password": "charlie_pass"},
    {"username": "david", "password": "david_pass"},
    {"username": "eve", "password": "eve_pass"}
]

for user in users:
    print(f"🔹 Registering {user['username']}...")

    # 1. Get nonce
    try:
        r = requests.get(f"{server_url}/_synapse/admin/v1/register")
        nonce = r.json()["nonce"]
    except Exception as e:
        print(f"❌ Failed to get nonce: {e}")
        continue

    # 2. Build mac
    user_str = user["username"]
    pass_str = user["password"]
    admin_flag = "notadmin"

    mac_str = f"{nonce}\x00{user_str}\x00{pass_str}\x00{admin_flag}"
    mac = hmac.new(
        key=shared_secret.encode(),
        msg=mac_str.encode(),
        digestmod=hashlib.sha1
    ).hexdigest()

    payload = {
        "nonce": nonce,
        "username": user_str,
        "password": pass_str,
        "mac": mac,
        "admin": False
    }

    res = requests.post(f"{server_url}/_synapse/admin/v1/register", json=payload)
    if res.status_code == 200:
        print(f"✅ Registered {user['username']}")
    else:
        print(f"❌ Error for {user['username']}: {res.json()}")

