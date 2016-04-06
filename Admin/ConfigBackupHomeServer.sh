#!/bin/sh

# TODO get rid of all this shit and write from scratch something normal

function create_new_backup {
	printf "Creating a new backup\n"
}

function dont_create_new_backup {
	printf "No crontab created. Aborting\n"
	exit
}

function unknown_command_entered {
	printf "Unknown command\n"
	exit
}

# check if the baskup is already set up
BACKUP_SET=$(cat /etc/crontab | grep BackupHomeServer.sh | grep -v grep)

if [ "$BACKUP_SET" = "" ]; then
	printf "No backup schedule found in crontab file. Create now?\nY/n\n"
	read CHOICE
fi

if [ "$CHOICE" = "Y" ]; then
	create_new_backup
elif [ "$CHOICE" = "n" ]; then
	dont_create_new_backup
else
	unknown_command_entered
fi
