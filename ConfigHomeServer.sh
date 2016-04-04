#!/bin/sh
DEFAULT_ADR="127.0.0.1"
DEFAULT_PORT="12345"
CONFIG_FILE="PyHomeServer.conf"

echo Please enter the address you want to use and press enter or press enter to use default one.
echo Default adress is: $DEFAULT_ADDR

read ADR

if [ "$ADR" = "" ]; then
    echo "Address: "$DEFAULT_ADR > $CONFIG_FILE
else
    echo "Address: "$ADR > $CONFIG_FILE
fi

echo Please enter the port you want to use and press enter or press enter to use default one.
echo default port number is: $DEFAULT_PORT

read PORT

if [ "$PORT" = "" ]; then
    echo "Port: "$DEFAULT_PORT >> $CONFIG_FILE
else
    echo "Port: ""$PORT" >> $CONFIG_FILE
fi

SERVER_PID=$(ps -ax | grep PyHomeServer.py | grep -v grep | awk '{print $1}')
if [ "$SERVER_PID" != "" ]; then
    kill -s SIGHUP $SERVER_PID
fi
exit 0
