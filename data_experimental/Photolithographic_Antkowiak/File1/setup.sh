#!/bin/bash
cd "$(dirname "$0")"

# get the read files
wget https://figshare.com/ndownloader/files/22305708 -O R1_original.fq.gz

# filter the reads for adapters, etc. with bbduk
../../../00_Tools/filter_single_reads.sh R1_original.fq.gz R1.fq.gz