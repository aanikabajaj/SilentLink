import sys
import os
import psycopg2  # Make sure this is imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("sys.path:", sys.path)  # DEBUG LINE

from db.db_config import DB_CONFIG, connect_to_db

def test_key_vault():
    try:
        # Connect to 'key_vault' database using your centralized function
        conn = connect_to_db("key_vault")
        if conn is None:
            print("❌ Could not establish connection.")
            return

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_keys;")
        rows = cursor.fetchall()
        print("✅ Fetched rows from encryption_keys:", rows)

        conn.close()
    except Exception as e:
        print("❌ Error testing key_vault schema:", e)

if __name__ == "__main__":
    test_key_vault()

