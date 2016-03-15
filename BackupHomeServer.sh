#!/bin/sh

# check if the baskup is already set up
BACKUP_SET=$(cat /etc/crontab | grep BackupHomeServer.sh | grep - v grep)

if [ $BACKUP_SET="" ]; then
	echo "Brak backupu"
else
	echo "Jest backup"
fi
