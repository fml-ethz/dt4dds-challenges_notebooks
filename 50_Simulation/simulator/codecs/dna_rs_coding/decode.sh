#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

# unzip
gunzip -c "$1" > "$1".unzip

# convert fastq to text
awk 'NR % 4 == 2' "$1".unzip > "$1".txt

# cluster sequences
echo "Performing clustering"
python "$BASE_PATH"/clustering.py "$1".txt "$1".txt.clusters
python "$BASE_PATH"/../../../../00_Tools/cluster2consensus_txt.py "$1".txt.clusters "$1".txt.clusters.consensus
mv "$1".txt "$1".txt.preclustering
mv "$1".txt.clusters.consensus "$1".txt

# trim and pad to sequence length
"$BASE_PATH"/../tool_padtrim/run.sh "$1".txt "$1".padtrim "$3"

# decode
"$BASE_PATH"/dna_rs_coding/simulate/texttodna --decode "${@:4}" --input="$1".padtrim --output="$2"

# remove intermediate files
rm -f "$1".txt.clusters.consensus
rm -f "$1".txt.clusters
rm -f "$1".unzip
rm -f "$1".txt
rm -f "$1".padtrim
rm -f "$1".txt.preclustering

exit