#!/bin/bash
shopt -s globstar
rm combined.hc22000
rm passwords.csv
rm passwords_wip.csv
hcxpcapngtool -o combined.hc22000 --max-essids=10 ./**/*.cap
hcxhashtool -i combined.hc22000 --info=stdout
hashcat -m 22000 combined.hc22000 --show --outfile passwords_wip.csv
hashcat --hwmon-temp-abort 100 -m 22000 -a 3 -d 1  --outfile  "./passwords_wip.csv"  "combined.hc22000"   "?h?h?h?h?h?h00"
./clean_passwords.sh passwords_wip.csv

