#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

# encode
"$BASE_PATH"/dna_rs_coding/simulate/texttodna --encode "${@:3}" --input="$1" --output="$2"

exit