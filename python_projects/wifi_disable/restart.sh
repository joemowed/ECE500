#!/bin/bash
INTERFACE="wlp0s20f3"
MON_INTERFACE="${INTERFACE}mon"
sudo airmon-ng stop $MON_INTERFACE 
sudo airmon-ng stop "wlan0mon"
sudo systemctl restart NetworkManager
