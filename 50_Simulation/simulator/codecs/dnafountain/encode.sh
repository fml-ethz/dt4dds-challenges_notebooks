#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

source "$BASE_PATH"/venv/bin/activate
python "$BASE_PATH"/dna-fountain/encode.py --file_in "$1" --out "$2" "${@:3}" -m 3 --gc 0.05 --rs 2 --delta 0.001 --c_dist 0.025

exit