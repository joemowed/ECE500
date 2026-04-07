#!/bin/bash
shopt -s globstar
rm combined.hc22000
rm passwords.csv
hcxpcapngtool -o combined.hc22000 --max-essids=10 --all ./**/*.cap
hcxhashtool -i combined.hc22000 --info=stdout
hashcat -m 22000 combined.hc22000 --show --outfile passwords.csv
hashcat --hwmon-temp-abort 100 -m 22000 -a 3 -d 1  --outfile  "./passwords.csv"  "combined.hc22000"   "?h?h?h?h?h?h00"

