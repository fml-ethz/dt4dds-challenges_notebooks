#!/bin/bash 
set -e
set -x

git clone https://github.com/Scilence2022/DBGPS_Python.git

cp encode_new.py DBGPS_Python/encode_new.py
cp decode_new.py DBGPS_Python/decode_new.py