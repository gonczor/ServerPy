#!/bin/sh
DEFAULT_NETWORK_INTERFACE="wlan0"
DEFAULT_ADR="127.0.0.1"
DEFAULT_PORT="12345"
DEFAULT_BACKUP_DIRECTORY="Backup"
CONFIG_FILE="Setup/settings.py"

echo Enter address you want to use. The list of available ports with interfaces is listed below.
ip -f inet addr | awk '{print  $2}' | grep -v forever

echo Please enter the address you want to use and press enter or press enter to use default one.
echo Default adress is: $DEFAULT_ADR

read ADR

if [ "$ADR" = "" ]; then
    echo "ADDRESS = '$DEFAULT_ADR'" > $CONFIG_FILE
else
    echo "ADDRESS = '$ADR'" > $CONFIG_FILE
fi

echo Please enter the port you want to use and press enter or press enter to use default one.
echo default port number is: $DEFAULT_PORT

read PORT

if [ "$PORT" = "" ]; then
    echo "PORT = $DEFAULT_PORT" >> $CONFIG_FILE
else
    echo "PORT = $PORT" >> $CONFIG_FILE
fi

echo "Please enter the directory you want to use to store server backup (running BackupServer.sh\
later on to finish configuration will be required)."
echo The default directory is $DEFAULT_BACKUP_DIRECTORY

read BACKUP_DIRECTORY

if [ "$BACKUP_DIRECTORY" = "" ]; then
    echo "BACKUP_DIR = '$DEFAULT_BACKUP_DIRECTORY'" >> $CONFIG_FILE
else
    echo "BACKUP_DIR = '$BACKUP_DIRECTORY'" >> $CONFIG_FILE
fi

# TODO implement backup setting

SERVER_PID=$(ps -ax | grep PyHomeServer.py | grep -v grep | awk '{print $1}')
if [ "$SERVER_PID" != "" ]; then
    kill -s SIGHUP $SERVER_PID
fi
exit 0
