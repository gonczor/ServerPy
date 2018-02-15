#!/bin/sh

SERVER_PID=$(pidof PyHomeServer.py)
if [ "$SERVER_PID" = "" ]; then
    echo "No Server process is running. Type ./PyHomeServer.py to run server."
else
    kill -s SIGINT $SERVER_PID
    echo "Waiting for server to stop..."
    while [ "$SERVER_PID" != "" ]; do
        SERVER_PID=$(pidof PyHomeServer.py)
    done
    echo "Server has been stopped successfully"
fi
