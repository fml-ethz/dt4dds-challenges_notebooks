#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

# add each sequence five times
awk '{for(i=0;i<5;i++) print}' "$1" > "$2"/R1.txt

# convert to fastq
dt4dds-utils txt2fastq "$2"/R1.txt "$2"/R1.fq

# compress
gzip -c "$2"/R1.fq > "$2"/R1.fq.gz

# remove intermediate files
rm -f "$2"/R1.txt
rm -f "$2"/R1.fq

exit