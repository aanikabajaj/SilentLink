#!/bin/bash

# Prompt for backup path
read -p "Enter backup directory path to restore from: " BACKUP_DIR

# Confirm backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Backup directory does not exist!"
    exit 1
fi

# Stop PostgreSQL before restore
sudo systemctl stop postgresql

# Restore PostgreSQL data using rsync
sudo rsync -a --delete "$BACKUP_DIR/postgresql/" /var/lib/postgresql/

# Start PostgreSQL
sudo systemctl start postgresql

# Log the restore event
echo "$(date): Restore completed from $BACKUP_DIR" >> /home/user/SilentLink/logs/backup_audit.log
