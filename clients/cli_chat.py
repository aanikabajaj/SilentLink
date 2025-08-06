# File: clients/cli_chat.py

import json
import os
import requests
from auth import login_user, switch_active_user
from messaging import send_message, view_messages

SESSION_PATH = "clients/session.json"
SERVER_URL = "http://localhost:8008"

def load_session():
    if not os.path.exists(SESSION_PATH):
        print("❌ session.json not found. Please run generate_session_json.py first.")
        return {}
    with open(SESSION_PATH) as f:
        return json.load(f)

def save_session(data):
    with open(SESSION_PATH, "w") as f:
        json.dump(data, f, indent=2)

def accept_invitation():
    session = load_session()
    active_user = session.get("active_user")
    user_data = session.get("users", {}).get(active_user)

    if not active_user or not user_data:
        print("❌ Please login or switch to an active user first.")
        return

    access_token = user_data.get("access_token")
    if not access_token:
        print("❌ Active user has no access token.")
        return

    user_id = user_data.get("user_id")

    # Step 1: Get joined/invited rooms
    url = f"{SERVER_URL}/_matrix/client/r0/sync?access_token={access_token}"
    resp = requests.get(url)
    if resp.status_code != 200:
        print("❌ Failed to fetch sync data:", resp.text)
        return

    data = resp.json()

    if "rooms" not in data or "invite" not in data["rooms"]:
        print("📭 No pending invitations found.")
        return

    invites = data["rooms"]["invite"]
    if not invites:
        print("📭 No pending invitations.")
        return

    print("📨 Pending Invitations:")
    room_ids = list(invites.keys())
    for i, room_id in enumerate(room_ids, 1):
        # Try to show a friendlier name if available
        name = room_id
        for event in invites[room_id]["invite_state"]["events"]:
            if event.get("type") == "m.room.name":
                name = event["content"].get("name", room_id)
                break
        print(f"{i}. {name} ({room_id})")

    try:
        selection = int(input("🔸 Enter number to accept invitation: ")) - 1
        selected_room = room_ids[selection]
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
        return

    # Join the room
    join_url = f"{SERVER_URL}/_matrix/client/r0/rooms/{selected_room}/join?access_token={access_token}"
    join_resp = requests.post(join_url, json={})
    
    if join_resp.status_code == 200:
        print(f"✅ Successfully joined room: {selected_room}")
    else:
        print(f"❌ Failed to join room: {join_resp.status_code} - {join_resp.text}")


def main_menu():
    print("""
🔐 SilentLink Terminal Chat
-----------------------------
1. Login (Refresh token)
2. Switch Active User
3. Send Message
4. View Messages
5. Show Current User
6. Exit
7. Create Room
8. Accept Room Invitation
9. View Decoy Messages
10. Send Decoy Messages
""")

def main():
    while True:
        main_menu()
        choice = input("🔸 Select an option: ").strip()

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_user(username, password)

        elif choice == "2":
            switch_active_user()

        elif choice == "3":
            send_message()

        elif choice == "4":
            view_messages()

        elif choice == "5":
            session = load_session()
            print("👤 Current active user:", session.get("active_user", "None"))

        elif choice == "6":
            print("👋 Exiting... Bye!")
            break

        elif choice == "7":
            os.system("python3 clients/create_room.py")

        elif choice == "8":
            accept_invitation()
            
        elif choice == "9":
            os.system("python3 scripts/view_decoy_messages.py")
            
        elif choice == "10":
            os.system("python3 scripts/send_decoy_messages.py")

        else:
            print("❗ Invalid option. Try again.")

if __name__ == "__main__":
    main()

