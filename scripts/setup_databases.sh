#!/bin/bash

# Day 1 – Setup script
# Run with: sudo ./setup_databases.sh

# Constants
DB_USER="silentlink_user"
DB_PASSWORD="ERYx@03_15"  # Replace later with .env for security
DB_LIST=(
  active_messages
  deleted_messages
  metadata
  key_vault
  decoy
  backup_metadata
  audit_log
  ephemeral_sessions
)

echo "Creating databases and user..."

# Create user and set password
sudo -u postgres psql -c "DO \$\$ BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    END IF;
END \$\$;"

# Loop to create each database and assign to user
for DB in "${DB_LIST[@]}"; do
    echo "Creating database: $DB..."
    sudo -u postgres createdb --lc-collate='C' --lc-ctype='C' --template=template0 "$DB"
    sudo -u postgres psql -d "$DB" -c "GRANT ALL PRIVILEGES ON DATABASE \"$DB\" TO $DB_USER;"
done

echo "✅ All databases created and user granted access."

