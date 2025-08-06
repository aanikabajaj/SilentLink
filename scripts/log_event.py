import psycopg2
from datetime import datetime
import sys

def log_event(event_type, event_detail):
    try:
        conn = psycopg2.connect(
            dbname="audit_log",
            user="silentlink_user",
            password="ERYx@03_15",
            host="127.0.0.1",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO audit_events (event_type, event_detail) VALUES (%s, %s)",
            (event_type, event_detail)
        )

        conn.commit()
        cur.close()
        conn.close()

        print(f"[{datetime.now()}] Logged event: {event_type} – {event_detail}")

    except Exception as e:
        print("Error logging event:", e)

# Run via: python log_event.py BACKUP "Backup completed at /backups/2025-08-06"
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python log_event.py EVENT_TYPE EVENT_DETAIL")
    else:
        log_event(sys.argv[1], sys.argv[2])
