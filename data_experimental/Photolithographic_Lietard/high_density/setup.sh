#!/bin/bash

# filter the reads for adapters, etc. with bbduk
../../../00_Tools/filter_paired_reads.sh R1_original.fq.gz R2_original.fq.gz R1.fq.gz R2.fq.gz