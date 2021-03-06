#!/usr/bin/env bash

# check if current directory contains the client and protocol modules which will be mounted along with parent dir

if [ ! -d "${PWD}/client" ] || [ ! -d "${PWD}/protocols" ]
then
    echo "Current directory ${PWD} does not contain at least one of: client or protocol modules"
    exit 1
fi

USAGE="Usage: $0 (start|stop|restart|status) <container_name>"

IMG_NAME="msc"
CONT_NAME=$2

RUNNING=$(docker inspect --format="{{ .State.Running }}" ${CONT_NAME} 2> /dev/null)

start_docker() {
    MSC_DIR="${PWD}"
    DOCKER_START="docker run -dit -v ${MSC_DIR}:/opt/msc --cap-add=NET_ADMIN --name=${CONT_NAME} --hostname=${CONT_NAME} ${IMG_NAME}"
    echo ${DOCKER_START}
    CONT_ID=$(${DOCKER_START})

    echo "Container ${CONT_NAME} (ID: ${CONT_ID}) has been started"
}

stop_docker() {
    docker stop ${CONT_NAME} > /dev/null
    docker rm ${CONT_NAME} > /dev/null

    echo "Container ${CONT_NAME} has been stopped"
}

login() {
    docker exec -it ${CONT_NAME} /bin/bash
}

if [[ $# != 2 ]]; then
    echo "No argument given"
    echo ${USAGE}
    exit
fi

case "$1" in
    "start")
        if [[ ! "${RUNNING}" =~ "true" ]]; then
            start_docker
        else
            echo "Container ${CONT_NAME} is running"
        fi ;;
    "stop")
        if [[ "${RUNNING}" =~ "true" ]]; then
            stop_docker
        else
            echo "Container ${CONT_NAME} is not running"
        fi ;;
    "restart")
        if [[ "${RUNNING}" =~ "true" ]]; then
            stop_docker
        fi
        start_docker ;;
    "status")
        if [[ "${RUNNING}" =~ "true" ]]; then
            echo "Container ${CONT_NAME} is running"
        else
            echo "Container ${CONT_NAME} is not running"
        fi ;;
    "login")
        if [[ "${RUNNING}" =~ "true" ]]; then
            login
        else
            echo "Container ${CONT_NAME} is not running"
        fi ;;
    *)
        echo "Invalid argument"
        echo ${USAGE}
        exit
esac
