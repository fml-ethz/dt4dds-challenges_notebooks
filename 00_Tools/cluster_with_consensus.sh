#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

gunzip -c "$1" > "$1".unzip
dt4dds-utils fastq2fasta "$1".unzip "$1".fasta

"$BASE_PATH"/mmseqs2/mmseqs easy-cluster "$1".fasta "$2".output "$1"_tmp -s 7.5 --max-seqs 5000 --cov-mode 1 -c 0.5 --cluster-mode 2 --min-seq-id 0.5 --threads 4
python "$BASE_PATH"/parse_clusters.py "$1".fasta "$2".output_cluster.tsv "$2".clusters
export PYTHONWARNINGS="ignore"
python "$BASE_PATH"/cluster2consensus.py "$2".clusters "$2"

rm -rf "$1"_tmp
rm -f "$1".unzip
rm -f "$1".fasta
rm -f "$2".output_all_seqs.fasta
rm -f "$2".output_rep_seq.fasta
rm -f "$2".output_cluster.tsv
rm -f "$2".clusters

exit
