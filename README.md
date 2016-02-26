# ServerPy
Server for communication with client in java. See the other repo for more info.

The server listens for connections on default port 12345. This can be changed by running ConfigHomeServer.sh which saves data into PyHomeServer.conf file.

The programme is notified about changes by calling a SIGTERM signal, which makes the whole server stop and be started again after waiting 60 seconds. It is necessary, since the singal handler is not available anymore after being called once. See signal(2) man page:
       On BSD,
       when a signal handler is invoked, the signal disposition is not
       reset, and further instances of the signal are blocked from being
       delivered while the handler is executing

The reason for implementing 60-second interval is to avoid the risk of comming into lost packets before the end of their lifetime.
