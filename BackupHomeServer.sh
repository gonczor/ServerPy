#!/bin/sh

# check if the baskup is already set up
BACKUP_SET=$(cat /etc/crontab | grep BackupHomeServer.sh | grep -v grep)

if [ $BACKUP_SET="" ]; then
	printf "No backup schedule found in crontab file. Create now?\nY/n"
	read CHOICE
else
	echo "GIT"
fi

echo $CHOICE
