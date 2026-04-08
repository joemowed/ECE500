#!/bin/bash

INTERFACE1="wlp0s20f3"
INTERFACE2="wlx289401b9b39f"

nmcli device wifi connect "0999-wombat" password "d3b5e800" ifname "$INTERFACE2" 
sudo ip addr add 192.168.1.100/24 dev "$INTERFACE2"
echo "Waiting for start...."
nc -l 9000 | head -n 1
echo "Starting Attack...."
exit
cleanup() {
    echo "Exiting...."
    trap - SIGINT SIGTERM
    kill -TERM -$$
}


trap cleanup SIGINT SIGTERM
nmcli device set "$INTERFACE1" autoconnect no
nmcli device set "$INTERFACE2" autoconnect no
./kill_subproc.sh passwords_pt1.csv "$INTERFACE1" &
./kill_subproc.sh passwords_pt2.csv "$INTERFACE2" &

wait
