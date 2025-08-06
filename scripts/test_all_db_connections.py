import sys
import os
import psycopg2

# Add ../db to the Python path so we can import db_config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db')))

from db_config import connect_to_db

# List of all 8 databases
databases = [
    "active_messages",
    "deleted_messages",
    "metadata",
    "key_vault",
    "decoy",
    "backup_metadata",
    "audit_log",
    "ephemeral_sessions"
]

def test_connections():
    print("🔍 Testing connections to all databases...\n")
    for db_name in databases:
        try:
            conn = connect_to_db(db_name)
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"✅ Connected to '{db_name}' successfully! PostgreSQL version: {version[0]}")
            cur.close()
            conn.close()
        except psycopg2.Error as e:
            print(f"❌ Failed to connect to '{db_name}': {e.pgerror or str(e)}")
        except Exception as e:
            print(f"⚠️ Unknown error while connecting to '{db_name}': {str(e)}")
    print("\n✅ Connection test complete.")

if __name__ == "__main__":
    test_connections()
