#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

mv "$1" "$1".unmerged
mv "$2" "$2".unmerged

"$BASE_PATH"/../../../00_Tools/ngmerge/ngmerge -1 "$1".unmerged -2 "$2".unmerged -o "$1" -d -e 10 -m 10 -z -v

exit