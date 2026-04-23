#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

INTERFACE1="wlp0s20f3"
INTERFACE2="wlx289401b9b39f"
echo "connecting to wombat..."
sudo nmcli device wifi connect "0999-wombat" password "d3b5e800" ifname "$INTERFACE1" 
echo "Setting IP ADDR"
sudo nmcli connection modify "0999-wombat" ipv4.address 192.168.125.100/24
sudo nmcli connection modify "0999-wombat" ipv4.method manual
sudo nmcli connection up "0999-wombat"
echo "connection finished..."
if [ifconfig | rg 192.168.125.100]; then
    echo "WARN: IP ADDRESS NOT FOUND"
else

    echo "INFO: ip addresss set successfull"
fi
echo "Waiting for start...."
nc -lp 9000 | head -n 1
echo "Starting Attack...."
cleanup() {
    echo "Exiting...."
    trap - SIGINT SIGTERM
    kill -TERM -$$
}


trap cleanup SIGINT SIGTERM
nmcli device set "$INTERFACE1" autoconnect no
nmcli device set "$INTERFACE2" autoconnect no
./kill_subproc.sh test.csv "$INTERFACE1" &
# ./kill_subproc.sh passwords_pt1.csv "$INTERFACE1" &
# ./kill_subproc.sh passwords_pt2.csv "$INTERFACE2" &

wait
