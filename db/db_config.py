import psycopg2

# Centralized DB credentials
DB_CONFIG = {   # <- CHANGED from DB_CREDENTIALS to DB_CONFIG
    "user": "silentlink_user",
    "password": "ERYx@03_15",
    "host": "localhost",
    "port": "5432",
}

VALID_DBS = [
    "active_messages",
    "deleted_messages",
    "metadata",
    "key_vault",
    "decoy",
    "backup_metadata",
    "audit_log",
    "ephemeral_sessions"
]

def connect_to_db(dbname):
    if dbname not in VALID_DBS:
        raise ValueError(f"Invalid database name: {dbname}")

    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        print(f"✅ Connected to database: {dbname}")
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to {dbname}: {e}")
        return None

