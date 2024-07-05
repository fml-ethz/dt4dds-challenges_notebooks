#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

# encode
python3 "$BASE_PATH"/DBGPS_Python/encode_new.py "${@:3}" --input="$1" --output="$2".fasta

# remove the first and last 18 characters of each line (ONLY FOR ESTIMATING CODING DENSITY)
# awk '{print substr($0, 19, length($0)-36)}' "$2".fasta > "$2".tmp

# only print every second row of the file
awk 'NR % 2 == 0' "$2".fasta > "$2"

# remove the temporary files
rm -f "$2".fasta.log
rm -f "$2".tmp
rm -f "$2".fasta

exit