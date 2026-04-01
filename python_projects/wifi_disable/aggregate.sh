#!/bin/bash
shopt -s globstar
rm essid_list.txt
rm combined.hc22000
hcxpcapngtool -o combined.hc22000 -E essid_list.txt --max-essids=10 --all ./**/*.cap
hcxhashtool -i combined.hc22000 --info=stdout

hashcat -m 22000 -a 3 -d 1 combined.hc22000  --show --outfile-format 1,2,3 ?h?h?h?h?h?h00

