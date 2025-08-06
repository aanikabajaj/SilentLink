from olm import Account
import psycopg2
import json
from datetime import datetime

def generate_user_keys(user_id):
    account = Account()
    account.generate_one_time_keys(5)

    identity_keys = account.identity_keys
    one_time_keys = account.one_time_keys
    pickle_data = account.pickle("your_secret_passphrase")

    conn = psycopg2.connect(
        dbname="key_vault", user="silentlink_user", password="ERYx@03_15", host="localhost"
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_keys (user_id, identity_keys, one_time_keys, session_pickle, last_rotated, rotation_count)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE
        SET identity_keys = EXCLUDED.identity_keys,
            one_time_keys = EXCLUDED.one_time_keys,
            session_pickle = EXCLUDED.session_pickle,
            last_rotated = EXCLUDED.last_rotated,
            rotation_count = user_keys.rotation_count + 1
    """, (
        user_id,
        json.dumps(identity_keys),
        json.dumps(one_time_keys),
        pickle_data,
        datetime.now(),
        1
    ))
    conn.commit()
    cur.close()
    conn.close()

# Example usage:
# generate_user_keys("alice@silentlink")
