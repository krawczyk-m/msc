#!/usr/bin/env bash

CMD=$1

docker_mgmt="${PWD}/docker_mgmt.sh"
rabbit_mgmt="${PWD}/rabbitmq_docker/rabbitmq-docker.sh"

if [ ! -f ${docker_mgmt} ] || [ ! -f ${rabbit_mgmt} ]
then
    echo "Either ${docker_mgmt} or ${rabbit_mgmt} do not exist!"
    exit 1
fi


setup() {
    bash ${docker_mgmt} start sender
    bash ${docker_mgmt} start receiver
    bash ${rabbit_mgmt} start
}

destroy() {
    bash ${docker_mgmt} stop sender
    bash ${docker_mgmt} stop receiver
    bash ${rabbit_mgmt} stop
}

case "${CMD}" in
    "setup")
        setup
        ;;
    "destroy")
        destroy
        ;;
    *)
        echo "Invalid argument"
        exit 1
esac

