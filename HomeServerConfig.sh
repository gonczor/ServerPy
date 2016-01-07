#!/bin/sh

DEFAULT_ADDR="127.0.0.1"
DEFAULT_PORT="12345"
CONFIG_FILE="PyHomeServer.conf"

echo Please enter the address you want to use and press enter or press enter to use default one.
echo default port number is: $DEFAULT_ADDR

read ADDR

if [ "$ADDR" = "" ]; then
    echo "Address: "$DEFAULT_ADDR > $CONFIG_FILE
else
    echo "Address: "$ADDR > $CONFIG_FILE
fi

echo Please enter the port you want to use and press enter or press enter to use default one.
echo default port number is: $DEFAULT_PORT

read PORT

if [ "$PORT" = "" ]; then
    echo "Port: "$DEFAULT_PORT >> $CONFIG_FILE
else
    echo "Port: ""$PORT" >> $CONFIG_FILE
fi

echo "conf changed" | nc -q 0 127.0.0.1 12345

exit 0