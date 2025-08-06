#!/bin/bash

# Encrypted Backup Location
BACKUP_DIR="/home/user/SilentLink/backups/$(date +%F_%T)"
mkdir -p "$BACKUP_DIR"

# PostgreSQL Data Directory
PG_DATA="/var/lib/postgresql"

# rsync: Create backup with preserved permissions
rsync -a --delete "$PG_DATA" "$BACKUP_DIR"

# Log to audit_log
echo "$(date): Backup completed at $BACKUP_DIR" >> /home/user/SilentLink/logs/backup_audit.log
