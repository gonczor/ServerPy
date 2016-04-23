#!/bin/bash

WORKING_DIRECTORY="$HOME/Documents/ServerPy"

function set_backup(){
    SCHEDULE_FILE="$WORKING_DIRECTORY/Configuration/crontab"
    SCHEDULE="* * * * *"
    USER=$(whoami)
    SCRIPT_NAME="$0"
    COMMAND='/bin/bash' #these spaces are essential for proper file formatting
    printf "$SCHEDULE " > $SCHEDULE_FILE
    printf " $USER " >> $SCHEDULE_FILE
    printf " $COMMAND " >> $SCHEDULE_FILE
    printf " $SCRIPT_NAME\n" >> $SCHEDULE_FILE
    crontab "$SCHEDULE_FILE"
}

function perform_backup(){
    BACKUP_FILENAME=$(date +%Y-%m-%d)
    BACKUP_FILENAME+=".tar.gz"
    BACKUP_DIR="$WORKING_DIRECTORY/"
    BACKUP_DIR+="$(cat $WORKING_DIRECTORY/Configuration/PyHomeServer.conf | grep "Backup directory:" |  awk '{print $3}')"

    echo "$BACKUP_DIR"
    FILES_TO_INCLUDE="$WORKING_DIRECTORY/Configuration/ $WORKING_DIRECTORY/Database/"
    echo Files to include
    echo "$FILES_TO_INCLUDE"
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir "$BACKUP_DIR"
    fi
	echo "I'm before taring"
    tar cvzpf "$BACKUP_DIR/$BACKUP_FILENAME" "$FILES_TO_INCLUDE"
	echo "And after"
}


function retrieve_latest_backup(){
    echo To be implemented
}

if [ $# -eq 0 ]; then
    perform_backup
elif [ "$1" = "retrieve" ]; then
    retrieve_latest_backup
elif [ "$1" = "set" ]; then
	set_backup
fi

