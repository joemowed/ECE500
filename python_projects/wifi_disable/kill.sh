INTERFACE="wlp0s20f3"
if nmcli --wait 5 device wifi connect "$ssid" password "$password" ifname "$INTERFACE" > /dev/null 2>&1; then
    # Manually assign an IP immediately (No waiting for DHCP!)
    # Adjust 192.168.1.50 to an IP likely to be free on your target networks
    sudo ip addr add 192.168.125.50/24 dev wlan0 2>/dev/null
    
    curl --connect-timeout 1 -s -X 'POST' 'http://192.168.125.1:8888/api/shutdown' 
    
    # Clean up the IP so the next network doesn't conflict
    sudo ip addr del 192.168.1.50/24 dev wlan0 2>/dev/null
fi
