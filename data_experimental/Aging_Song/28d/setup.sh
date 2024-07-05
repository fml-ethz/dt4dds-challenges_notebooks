#!/bin/bash

# get the read files
#wget https://figshare.com/ndownloader/files/33280562 -O R1_original.fq.gz
#wget https://figshare.com/ndownloader/files/33280925 -O R2_original.fq.gz

# filter the reads for adapters, etc. with bbduk
../../../00_Tools/filter_paired_reads.sh R1_original.fq.gz R2_original.fq.gz R1_filtered.fq.gz R2_filtered.fq.gz

# merge the paired reads 
../../../00_Tools/merge_reads.sh R1_filtered.fq.gz R2_filtered.fq.gz R1.fq.gz