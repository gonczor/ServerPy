#!/bin/sh

function set_backup(){
    SCHEDULE_FILE="Configuration/crontab"
    SCHEDULE="* * * * *"
    USER=$(whoami)
    WORKING_DIRECTORY="$PWD"
    SCRIPT_NAME="/Admin/BackupHomeServer.sh"
    COMMAND=' /bin/bash ' #these spaces are essential for proper file formatting
    printf "$SCHEDULE " > $SCHEDULE_FILE
    #printf "$USER" >> $SCHEDULE_FILE
    printf "$COMMAND" >> $SCHEDULE_FILE
    printf "$WORKING_DIRECTORY" >> $SCHEDULE_FILE
    printf "$SCRIPT_NAME\n" >> $SCHEDULE_FILE
    crontab $SCHEDULE_FILE
}

function perform_backup(){
    BACKUP_FILENAME=$(date +%Y-%m-%d)
    BACKUP_FILENAME+=".tar.gz"
    BACKUP_DIR=$(cat Configuration/PyHomeServer.conf | grep "Backup directory:" |  awk '{print $3}')

    FILES_TO_INCLUDE="Configuration/ Database/"
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir $BACKUP_DIR
    fi
    tar -cvzpf $BACKUP_DIR/$BACKUP_FILENAME $FILES_TO_INCLUDE
}


function retrieve_latest_backup(){
    echo To be implemented
}

if [ "$#" = "0" ]; then
    perform_backup
elif [ "$1" = "retrieve" ]; then
    retrieve_latest_backup
elif [ "$1" = "set" ]; then
	set_backup
fi

