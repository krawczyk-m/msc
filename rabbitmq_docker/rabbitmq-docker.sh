#!/usr/bin/env bash

USAGE="Usage: $0 (start|stop|restart|status)"

IMG_NAME="msc_rabbit"
CONT_NAME=${IMG_NAME}

RUNNING=$(docker inspect --format="{{ .State.Running }}" ${IMG_NAME} 2> /dev/null)

start_docker() {
    DOCKER_START="docker run -d -p 5672:5672 -p 15672:15672 --name=${CONT_NAME} -e RABBITMQ_ERLANG_COOKIE='cookie' ${IMG_NAME}"
    echo ${DOCKER_START}
    CONT_ID=$(${DOCKER_START})

    echo "Container ${CONT_NAME} (ID: ${CONT_ID}) has been started"
}

stop_docker() {
    docker stop ${CONT_NAME} > /dev/null
    docker rm ${CONT_NAME} > /dev/null

    echo "Container ${CONT_NAME} has been stopped"
}

if [[ $# != 1 ]]; then
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
    *)
        echo "Invalid argument"
        echo ${USAGE}
        exit
esac
