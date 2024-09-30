#!/bin/bash 
cd "$(dirname "$0")"
set -e
set -x

# git clone https://github.com/reinhardh/dna_rs_coding.git
git clone https://github.com/agimpel/dna_rs_coding.git
cd ./dna_rs_coding/simulate
make texttodna
