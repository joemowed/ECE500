#!/bin/bash
# INTERFACE="wlp0s20f3"
INTERFACE="wlx289401b9b39f"

FILE="$1"

# Check if file exists
[[ ! -f "$FILE" ]] && echo "File not found!" && exit 1

# Read the file line by line
# -r prevents backslash escapes from being interpreted
while IFS=',' read -r col1 col2 col3; do
    echo "Processing: $col1"
    echo "Data: $col2 and $col3"
    echo "---"
done < "$FILE"
exit
ssid="0999-wombat"
password="d3b5e800"
nmcli device disconnect $INTERFACE
if nmcli --wait 5 device wifi connect "$ssid" password "$password" ifname "$INTERFACE" ; then
    # Manually assign an IP immediately (No waiting for DHCP!)
    # Adjust 192.168.1.50 to an IP likely to be free on your target networks
    # sudo timeout 1s ip addr add 192.168.125.50/24 dev "$INTERFACE" 
    
    timeout 1.5s curl --connect-timeout 1 -s -X 'POST' 'http://192.168.125.1:8888/api/shutdown' 
    
    # Clean up the IP so the next network doesn't conflict
    # sudo timeout 1s ip addr del 192.168.1.50/24 dev "$INTERFACE" 
fi
