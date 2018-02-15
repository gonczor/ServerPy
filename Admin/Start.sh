#!/usr/bin/env bash

SERVER_PID=$(pidof PyHomeServer.py)

if [ "$SERVER_PID" = "" ]; then
    printf "Starting server..."
    python3 ./PyHomeServer.py
else
    printf "Server is already running. Process ID is: $SERVER_PID"
fi
