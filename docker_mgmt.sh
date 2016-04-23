#!/usr/bin/env bash

USAGE="Usage: $0 (start|stop|restart|status)"

IMG_NAME="msc"
CONT_NAME=$2

RUNNING=$(docker inspect --format="{{ .State.Running }}" ${CONT_NAME} 2> /dev/null)

start_docker() {
    DOCKER_START="docker run -dit --cap-add=NET_ADMIN --name=${CONT_NAME} ${IMG_NAME} /bin/bash"
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
