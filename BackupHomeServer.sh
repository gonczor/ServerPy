#!/bin/sh

# how this shit will work:
# checks whether setup mode (-s or --set) has been chosen
# if yes asks for:
#   -directory to store backup
#   -time interval between backups

function set_backup(){
    echo 'set'
}

function perform_backup(){
    DATE=$(date +%Y-%m-%d)
    DATE+=".tar.gz"
    if [ ! -d "Backup" ]; then
        mkdir Backup
    fi
    tar -cpzf Backup/$DATE Test
}

function show_help(){
    cat help
}

if [ "$#" = 0 ]; then
    perform_backup
elif [ "$1" = "-s" ] || [ "$1" = "--set" ]; then
    set_backup
elif [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
else
    echo "Unknown command. Run script with -h to show help."
fi

