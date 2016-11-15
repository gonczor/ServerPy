#!/bin/bash

function create_production_ssl_certs(){
    # TODO implement
    echo "Not implemented"
}


function create_test_ssl_certs(){
    sudo openssl req -new > new.ssl.csr
    sudo openssl rsa -in privkey.pem -out new.cert.key
    sudo openssl x509 -in new.ssl.csr -out new.cert.cert -req -signkey new.cert.key -days 999
    if [ ! -d Configuration/SSL ]; then
        mkdir Configuration/SSL
    fi
    sudo cp new.cert.cert Configuration/SSL/server.crt
    sudo cp new.cert.key Configuration/SSL/server.key
    sudo rm new.ssl.csr
    sudo rm new.cert.cert
    sudo rm new.cert.key
    sudo rm privkey.pem
}

if [ $# -eq 0 ]; then
    create_production_ssl_certs
elif [ "$1" = "test" ]; then
    create_test_ssl_certs
fi
