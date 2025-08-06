# File: scripts/view_decoy_messages.py

import psycopg2

conn = psycopg2.connect(
    dbname="decoy",
    user="silentlink_user",
    password="ERYx@03_15",
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()
cur.execute("SELECT sender, room_id, content, timestamp, sent FROM decoy_messages ORDER BY timestamp DESC LIMIT 10")
rows = cur.fetchall()

print("\n🕵️ Recent Decoy Messages:\n")
for row in rows:
    sent_status = "✅ Sent" if row[4] else "❌ Not Sent"
    room_display = row[1] if row[1] else "(no room)"
    msg_display = row[2] if row[2] else "(no content)"
    print(f"👤 {row[0]} in {room_display}: {msg_display} ({row[3]}) [{sent_status}]")

cur.close()
conn.close()

