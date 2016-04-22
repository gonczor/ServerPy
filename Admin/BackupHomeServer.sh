#!/bin/sh

function set_backup(){
    echo 'set' > "Configuration/crontab"
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

if [ "$#" = 0 ]; then
    perform_backup
elif [ "$1" = "retrieve" ]; then
    retrieve_latest_backup
elif [ "$1" = "set" ]; then
	set_backup
fi

