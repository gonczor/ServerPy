#!/bin/bash

#TODO
# *allow user to choose how often and when they want backups
# *allow change of working directory
#
# possibly this will be done in a separate python program
WORKING_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

function set_backup(){
    SCHEDULE_FILE=$WORKING_DIRECTORY/Configuration/crontab
    echo "schedule file: $SCHEDULE_FILE"
    SCHEDULE="* * * * *"
    SCRIPT_NAME=$WORKING_DIRECTORY/$0
    COMMAND='/bin/bash' #these spaces are essential for proper file formatting
    printf "$SCHEDULE " > $SCHEDULE_FILE
    printf " $COMMAND " >> $SCHEDULE_FILE
    printf " $SCRIPT_NAME\n" >> $SCHEDULE_FILE
    crontab "$SCHEDULE_FILE"
}

function perform_backup(){
    BACKUP_FILENAME=$(date +%Y-%m-%d)
    BACKUP_FILENAME+=".tar.gz"
    BACKUP_DIR="$WORKING_DIRECTORY/"
    BACKUP_DIR+="$(cat $WORKING_DIRECTORY/Setup/settings.py | grep "BACKUP_DIR = " |  awk '{print $3}')"
    BACKUP_DIR="$(echo $BACKUP_DIR | sed "s/['\"]//g")"
    echo $BACKUP_DIR

    FILES_TO_INCLUDE=$WORKING_DIRECTORY/Configuration
    FILES_TO_INCLUDE+=" "

    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir "$BACKUP_DIR"
    fi

    tar -cpzvf $BACKUP_DIR/$BACKUP_FILENAME $FILES_TO_INCLUDE
	
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

