#!/bin/sh

SERVER_PID=$(ps -ax | grep PyHomeServer.py | grep -v grep | awk '{print $1}')
kill -s SIGINT $SERVER_PID
