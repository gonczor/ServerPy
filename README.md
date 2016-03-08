# ServerPy
Server for communication with client in java. See the other repo for more info.

The server listens for connections on default port 12345. This can be changed by running ConfigHomeServer.sh which saves data into PyHomeServer.conf file.

The programme is notified about changes by calling a SIGHUP signal called from ConfigHomeServer.sh, which makes the whole server close connections and restart them after waiting 60 seconds. It is cused by default waiting time, which disallows creating new connections. It is due to make sure that any lost packets will come to the end of the lifetime before setting up a new connection (that's why I chose this option rather than allowing the reuse of address).

Programme is killed by calling SIGINT from StopHomeServer.sh script.

The loop and flags are used to allow sending signals multiple times. It is necessary, since the singal handler is not available anymore after being called once. See signal(2) man page:
       On BSD,
       when a signal handler is invoked, the signal disposition is not
       reset, and further instances of the signal are blocked from being
       delivered while the handler is executing
