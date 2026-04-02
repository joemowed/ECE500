#!/bin/bash
shopt -s globstar
rm combined.hc22000
rm passwords.csv
hcxpcapngtool -o combined.hc22000 --max-essids=10 --all ./**/*.cap
hcxhashtool -i combined.hc22000 --info=stdout
hashcat -m 22000 -a 3 -d 1 --potfile-disable --outfile ./passwords.csv  combined.hc22000   ?h?h?h?h?h?h00

