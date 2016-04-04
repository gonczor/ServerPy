#!/bin/sh

function set_backup(){
    echo 'set'
}

function perform_backup(){
    BACKUP_FILENAME=$(date +%Y-%m-%d)
    BACKUP_FILENAME+=".tar.gz"
    BACKUP_DIR=$(cat PyHomeServer.conf | grep "Backup directory:" |  awk '{print $3}')
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir $BACKUP_DIR
    fi
    tar -cpzf $BACKUP_DIR/$BACKUP_FILENAME Test
}

function show_help(){
    cat help
}

function retrieve_latest_backup(){
    echo To be implemented
}

if [ "$#" = 0 ]; then
    perform_backup
elif [ "$1" = "-s" ] || [ "$1" = "--set" ]; then
    set_backup
elif [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
elif [ "$1" = "-r" ] || [ "$1" = "--retrieve" ]; then
    retrieve_latest_backup
else
    echo "Unknown command. Run script with -h to show help."
fi

