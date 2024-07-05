#!/bin/bash 
set -e
set -x
BASE_PATH="$(dirname -- "${BASH_SOURCE[0]}")"

"$BASE_PATH"/bbmap/bbduk.sh -Xmx4g in1="$1" out1="$2" t=4 ref=adapters ktrim=r k=23 mink=11 hdist=1 tpe tbo >& bbduk.log

exit