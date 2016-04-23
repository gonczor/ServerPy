#!/usr/bin/env bash

# This script is used for launching server and configuration scripts from Admin/ directory.
# See Admin/help or README.md for further details.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "$#" = 0 ] || [ "$1" = "start" ]; then
    bash "$DIR/Admin/Start.sh"
elif [ "$1" = "config" ]; then
    bash "$DIR/Admin/ConfigHomeServer.sh"
elif [ "$1" = "help" ]; then
    cat "$DIR/Admin/help"
elif [ "$1" = "stop" ]; then
    bash "$DIR/Admin/StopHomeServer.sh"
elif [ "$1" = "backup" ]; then
    bash $DIR/Admin/BackupHomeServer.sh $2
else
    echo "Unknown command. Run script with \"help\" to display help."
fi
