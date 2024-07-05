#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

"$BASE_PATH"/ngmerge/ngmerge -1 "$1" -2 "$2" -o "$3" -m 10 -d -e 10 -z -n 4 -f fail -v >& ngmerge.log

exit