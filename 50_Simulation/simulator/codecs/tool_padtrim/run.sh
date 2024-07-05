#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

python "$BASE_PATH"/padtrim.py "$@"
exit