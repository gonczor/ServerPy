#!/usr/bin/env bash

SERVER_PID=$(ps -ax | grep PyHomeServer.py | grep -v grep | awk '{print $1}')

if [ "$SERVER_PID" = "" ]; then
    ../PyHomeServer.py
else
    printf "Server is already running. Process ID is: $SERVER_PID"
fi