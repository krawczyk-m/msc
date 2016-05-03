#!/bin/bash

PORT=$1
# Prepend "nc" if the first argument is not an executable
if ! type -- "$1" &> /dev/null; then
    set -- nc -lk "$@"
fi

iptables -I INPUT -p tcp -m tcp --dport ${PORT} -m connbytes --connbytes-mode packets --connbytes-dir both --connbytes 4 -j NFQUEUE --queue-num 1
iptables -I OUTPUT -p tcp -m tcp --dport ${PORT} -m connbytes --connbytes-mode packets --connbytes-dir both --connbytes 4 -j NFQUEUE --queue-num 2

is_steganography_installed=`pip freeze | grep Steganography`

if [ $? != 0 ] # not
then
   echo "not installed" > /tmp/out
   cd /opt/msc && python setup.py develop
fi

exec "$@"