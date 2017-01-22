# ServerPy

This project provides server for intelligent home. It collects data from end devices (such as plant watering controller) and provides access to this data and control from outside from for example from Android device. This project takes security seriously, so SSL and proper authentication and password handling is crucial.

Basic actions are called from server.sh bash script with adequate options.

 * No options or "start" options: start server. Script ensures only one instance of the server is run at a time so use it instead of PyHomeServer.py to run server.
 * "config" configure server, this option restarts server automatically. It takes one minute for deterministic performance reasons.
 * "stop" shutdown server
 * "backup" perform backup immediately
 * "backup retrieve" retrieve data from latest backup (in future defining date to retieve it will be introduced)
 * "backup set" setup backup

Configuration is stored in Configuration/PyHomeServer.conf. Currently it allows to define desired IP address for the server and port for listening. In future it will also hold backup storage directory and crontab config for backups. Currently it is hardcoded.

# For contributors

For information please contact me at wiktor.gonczaronek [at] gmail.com

The project aims at providing services for intelligent home and serve some educational purposes. Therefore everyone is welcome to contribute as long as they follow certain rules:
1. I don't like bad code. If you think you will make a pull request with a 100 line long function with 5 nested ifs, or with variable named like "mkdfs", don't even touch the keyboard.
2. You have to be willing to learn something. Don't know what you can do? Contact me and we'll talk.
3. You don't have to know anything. Even working with git. I'll suggest you proper materials and I'm happy to answear questions as long as you show willingness to challenge your skills.

Reported issues are assigned in my trello page for dealing with this project, but you can make a single pull request without signing up if you want.

Workflow

If you start working on any issue pull latest changes from develop branch and checkout to new branch named as follows:
 * for new features add feat/<issue name>
 * for correcting bugs bug/<issue name>
So if you detect eg. authentication error make new branch bug/authentication_bug, if you want to add better sql database handling make feat/improve_sql_handling.

# Administration

For administration purposes bash scripts have been introduced. All are stored in Admin/ directory.

# Network handling

Core is done in ConnectionHandler.py. It handles multithreading via pyhon socketserver module as well as ssl communication. The communication process goes as follows:
1. User connects to the server and sends credentials.
2. If password is OK, the server sends proper handshake and awaits orders.
3. Orders from user are performed until user shuts down connection.

If user enters invalid password or send incorret order connection is shut down and IP address is banned. Ban handling is performed by BannedAddressesCache.py.

Orders currently available are:
 * welcome: send welcome message;
 * send file: send example file;
 * setpump: set pump parameters.

# Database handling
Currently not implemented.

# Authentication
Server uses SSL for secure communication with self-signed certs. To generate one simply type <b>./server.sh ssl test</b> (since it's still being tested, but is useful for home appliances). The cert and pem files will be generated in Configuration/SSL directory. You need .crt file on your customer application to communicate with server.
<br>
When it comes to username and password... Well... Type in user/pass to get in. This still requires implementation.

# Embedded handling

Raspberry Pi uses NRF24L01 radio to communicate with end devices.

It's server's duty to handle entire process. It starts with sending message to Arduino. Current options are:
<ul>
<li>GETSTATE - request for state
<li> SETPUMPxxxxyyyy - set pump parameters.
</ul>

The pump is actual pump connected to arduino that is on the other side of wave. It allows to set two parameters.
While setting pump parameters x's are 4 digits base-10 that represent how long (in seconds) the pump is set on after detecting that soil is dry.
Y's represent how long (in seconds) the pump remains inactive after doing pumping. See <a href="https://github.com/gonczor/watering/tree/master">  this project page</a> for further reference.
