#!/bin/bash

# get the read files
wget ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR526/ERR5265254/normal_S1_L001_R1_001.fastq.gz -O R1_original.fq.gz
wget ftp://ftp.sra.ebi.ac.uk/vol1/run/ERR526/ERR5265254/normal_S1_L001_R2_001.fastq.gz -O R2_original.fq.gz

# filter the reads for adapters, etc. with bbduk
../../../00_Tools/filter_paired_reads.sh R1_original.fq.gz R2_original.fq.gz R1.fq.gz R2.fq.gz