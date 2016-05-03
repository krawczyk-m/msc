#!/usr/bin/env bash

docker_mgmt="${PWD}/docker_mgmt.sh"
rabbit_mgmt="${PWD}/rabbitmq_docker/rabbitmq-docker.sh"

if [ ! -f ${docker_mgmt} ] || [ ! -f ${rabbit_mgmt} ]
then
    echo "Either ${docker_mgmt} or ${rabbit_mgmt} do not exist!"
    exit 1
fi


bash ${docker_mgmt} start sender
bash ${docker_mgmt} start receiver
bash ${rabbit_mgmt} start