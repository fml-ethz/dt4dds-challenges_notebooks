#!/bin/bash 

# run simulation
../../00_Tools/dt4dds-challenges/dt4dds-challenge photolithography ./design_files.fasta ./R1.fq ./R2.fq -f fastq --physical_redundancy 200 --sequencing_depth 200

# zip the output
gzip R1.fq
gzip R2.fq

# move the sequencing output
mv R1.fq.gz R1_original.fq.gz
mv R2.fq.gz R2_original.fq.gz

# filter the reads for adapters, etc. with bbduk
../../00_Tools/filter_paired_reads.sh R1_original.fq.gz R2_original.fq.gz R1.fq.gz R2.fq.gz

# analyze the reads
dt4dds-analysis . -c photolithographic -p -f