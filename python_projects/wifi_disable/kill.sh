#!/bin/bash
cleanup() {
    echo "Exiting...."
    kill -TERM -$$
}

INTERFACE1="wlp0s20f3"
INTERFACE2="wlx289401b9b39f"
trap cleanup SIGINT SIGTERM
./kill_subproc.sh passwords.csv "$INTERFACE1" &
./kill_subproc.sh passwords.csv "$INTERFACE2" &


