#!/bin/bash

# Define the backup directory and the maximum number of backups
BACKUP_DIR=~/moonshot/backups
MAX_BACKUPS=5

# Check if the moonshot directory exists
if [ ! -d ~/moonshot/moonshot ]; then
  echo "Skip backup: ~/moonshot/moonshot dir does not exist."
  exit 0
fi

# Create the backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Find the highest existing backup number
highest_backup=$(ls $BACKUP_DIR | grep -oP 'backup_\d+' | grep -oP '\d+' | sort -n | tail -1)
highest_backup=${highest_backup:-0}

# If the number of backups is less than the maximum, increment the highest backup number
if [ $(ls $BACKUP_DIR | wc -l) -lt $MAX_BACKUPS ]; then
  new_backup=$((highest_backup + 1))
else
  # If the number of backups is equal to the maximum, delete the oldest backup and shift the remaining backups
  oldest_backup=$(ls $BACKUP_DIR | grep -oP 'backup_\d+' | grep -oP '\d+' | sort -n | head -1)
  rm -rf $BACKUP_DIR/backup_$oldest_backup
  for i in $(seq $((oldest_backup + 1)) $highest_backup); do
    mv $BACKUP_DIR/backup_$i $BACKUP_DIR/backup_$((i - 1))
  done
  new_backup=$highest_backup
fi

# Create a new backup by moving the moonshot directory to the backup directory with the new backup number
mv ~/moonshot/moonshot $BACKUP_DIR/backup_$new_backup
