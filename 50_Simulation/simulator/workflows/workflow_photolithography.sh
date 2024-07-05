#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

# run the digital twin
"$BASE_PATH"/dt4dds-challenges/dt4dds-challenges photolithography "$1" "$2"/R1.fq "$2"/R2.fq -f fastq --strict

# zip the output
gzip "$2"/R1.fq
gzip "$2"/R2.fq

# merge the forward and reverse reads
"$BASE_PATH"/run_ngmerge.sh "$2"/R1.fq.gz "$2"/R2.fq.gz

exit