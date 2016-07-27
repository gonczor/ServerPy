#!/bin/sh

SERVER_PID=$(ps -ax | grep PyHomeServer.py | grep -v grep | awk '{print $1}')
if [ "$SERVER_PID" = "" ]; then
    echo "No Server process is running. Type ./PyHomeServer.py to run server."
else
    kill -s SIGINT $SERVER_PID
    echo "Waiting for server to stop..."
    while [ "$SERVER_PID" != "" ]; do
        SERVER_PID=$(ps -ax | grep PyHomeServer.py | grep -v grep | awk '{print $1}')
    done
    echo "Server has been stopped successfully"
fi
