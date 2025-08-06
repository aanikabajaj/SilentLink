from olm import Account
import psycopg2
import json
from datetime import datetime

def rotate_keys(user_id):
    account = Account()
    account.generate_one_time_keys(5)
    new_keys = account.one_time_keys

    conn = psycopg2.connect(
        dbname="key_vault", user="silentlink_user", password="ERYx@03_15", host="localhost"
    )
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_keys
        SET one_time_keys = %s,
            last_rotated = %s,
            rotation_count = rotation_count + 1
        WHERE user_id = %s
    """, (
        json.dumps(new_keys),
        datetime.now(),
        user_id
    ))
    conn.commit()
    cur.close()
    conn.close()
