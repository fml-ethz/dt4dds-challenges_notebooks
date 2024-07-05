#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

# unzip
gunzip -c "$1" > "$1".unzip

# convert fastq to text
awk '(NR%4==2){print $0}' "$1".unzip > "$1".txt

# filter and sort sequences by abundance
sort -S4G "$1".txt | uniq -c > "$1".select.sorted
sed -r 's/^\s+//' "$1".select.sorted | sort -r -n -k1 -S4G > "$1".select.sorted.quantity
cut -f2 -d' ' "$1".select.sorted.quantity | grep -v 'N' > "$1".select.sorted.seq

# remove sequences which are too short
awk -v design_length="$3" 'length($0) >= design_length' "$1".select.sorted.seq > "$1".select.sorted.seq.filtered

# add the reverse-complement of each sequence to a separate file
awk '{print $0}' "$1".select.sorted.seq.filtered | rev | tr "ATCG" "TAGC" > "$1".select.sorted.seq.filtered.rc

# interleave the two files
# paste -d '\n' "$1".select.sorted.seq.filtered "$1".select.sorted.seq.filtered.rc > "$1".select.sorted.seq.filtered.all

# add the reverse complement to the end of the file
cat "$1".select.sorted.seq.filtered "$1".select.sorted.seq.filtered.rc > "$1".select.sorted.seq.filtered.all

# trim and pad to sequence length
"$BASE_PATH"/../tool_padtrim/run.sh "$1".select.sorted.seq.filtered.all "$1".padtrim "$3"

# decode
source "$BASE_PATH"/venv/bin/activate
python "$BASE_PATH"/dna-fountain/decode.py --file_in "$1".padtrim --out "$2" "${@:4}" --header_size 4 --rs 2 --delta 0.001 --c_dist 0.025 -m 3 --gc 0.05 --max_hamming 100

# remove intermediate files
# rm -f "$1".unzip
# rm -f "$1".txt
# rm -f "$1".padtrim
# rm -f "$1".select.sorted
# rm -f "$1".select.sorted.quantity
# rm -f "$1".select.sorted.seq
# rm -f "$1".select.sorted.seq.filtered
# rm -f "$1".select.sorted.seq.filtered.rc
# rm -f "$1".select.sorted.seq.filtered.all

exit
