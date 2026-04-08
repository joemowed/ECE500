#!/bin/bash
# Check if a filename was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi
awk -F':' '{print $4 "," $5}' "$1" | sort -u > passwords.csv
