#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

# unzip
gunzip -c "$1" > "$1".unzip

# decode from fastq
python3 "$BASE_PATH"/DBGPS_Python/decode_new.py "${@:3}" --input="$1".unzip --output="$2" --type=fastq

# remove the temporary files
rm -f "$1".unzip

exit