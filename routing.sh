#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

USAGE="Usage: $0 (setup|clear)"

cmd=$1

# this apparently counts packets in both directions
# but redirects packets to NFQUEUE only destined to port 1234
setup() {
    # allow to set up tcp connection, redirect to NFQUEUE each packet after the 3rd one
    iptables -I INPUT -p tcp -m tcp --dport 1234 -m connbytes --connbytes-mode packets --connbytes-dir both --connbytes 4 -j NFQUEUE --queue-num 1
}

clear() {
    iptables -L INPUT | grep NFQUEUE &> /dev/null
    while [[ $? -ne 1 ]]; do
        iptables -D INPUT 1
        iptables -L INPUT | grep NFQUEUE &> /dev/null
    done
}

if [[ ! "$cmd" =~ "" ]]; then
    echo "No command given"
    echo ${USAGE}
    exit
fi

case "$cmd" in
    "setup")
            setup
            ;;
    "clear")
            clear
            ;;
    *)
        echo "Invalid argument"
        echo ${USAGE}
        exit 1
esac
